#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import numpy as np
from sklearn.ensemble import RandomForestClassifier

STABILITY_THRESHOLD = 3


def train_ml_model():
    """
    Train a simple RandomForest on representative sensor data.
    Labels:  0 = RUNNING,  1 = WARNING,  2 = STOP SYSTEM

    In a real deployment you would load a pre-trained model from disk.
    This inline training gives consistent, deterministic behaviour for
    demonstration and integration testing.
    """
    # [temp, vibration, load]
    X = np.array([
        # normal → RUNNING (0)
        [55.0, 1.5, 3.0],
        [60.0, 2.0, 4.0],
        [65.0, 2.5, 5.0],
        [58.0, 1.8, 3.5],
        [62.0, 2.2, 4.5],
        [50.0, 1.0, 2.5],
        [57.0, 1.6, 3.2],

        # borderline → WARNING (1)
        [72.0, 4.0, 8.5],
        [74.0, 4.5, 9.0],
        [70.0, 3.8, 8.0],
        [73.0, 4.2, 8.8],

        # critical → STOP SYSTEM (2)
        [85.0, 6.5, 12.0],
        [90.0, 7.0, 13.0],
        [88.0, 8.0, 14.0],
        [82.0, 6.0, 11.5],
        [95.0, 9.0, 15.0],
    ])

    y = np.array([0, 0, 0, 0, 0, 0, 0,
                  1, 1, 1, 1,
                  2, 2, 2, 2, 2])

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    return model


ML_LABELS = {0: 'RUNNING', 1: 'WARNING', 2: 'STOP SYSTEM'}


class MonitorNode(Node):

    def __init__(self):
        super().__init__('monitor_node')

        # train model once at startup
        self.model = train_ml_model()
        self.get_logger().info('ML model ready')

        # subscribers
        self.create_subscription(String, '/sensor/temperature', self.temp_cb,  10)
        self.create_subscription(String, '/sensor/vibration',   self.vib_cb,   10)
        self.create_subscription(String, '/sensor/load',        self.load_cb,  10)

        # publisher
        self.pub = self.create_publisher(String, '/system_action', 10)

        # latest parsed sensor data: {name: (value, state)}
        self.sensor_data = {
            'temperature': (0.0, 'normal'),
            'vibration':   (0.0, 'normal'),
            'load':        (0.0, 'normal'),
        }

        # track first message received per sensor
        self.received = {'temperature': False, 'vibration': False, 'load': False}

        # stability filter
        self.current_state   = 'RUNNING'
        self.last_candidate  = 'RUNNING'
        self.counter         = 0

        self.timer = self.create_timer(1.0, self.evaluate)
        self.get_logger().info('monitor_node started')

    # ── parsing ───────────────────────────────────────────────────────────────

    def parse(self, raw: str, name: str):
        """
        Parse "value,state" format.
        Returns (float, str) or None on failure.
        Never silently swallows errors.
        """
        try:
            parts = raw.strip().split(',')
            if len(parts) != 2:
                raise ValueError(f'expected 2 parts, got {len(parts)}')
            value = float(parts[0].strip())
            state = parts[1].strip().lower()
            if state not in ('normal', 'abnormal'):
                raise ValueError(f'unknown state "{state}"')
            return value, state
        except Exception as e:
            self.get_logger().warn(f'[{name}] parse error — "{raw}" — {e}')
            return None

    # ── sensor callbacks ──────────────────────────────────────────────────────

    def temp_cb(self, msg):
        result = self.parse(msg.data, 'temperature')
        if result:
            self.sensor_data['temperature'] = result
            self.received['temperature'] = True

    def vib_cb(self, msg):
        result = self.parse(msg.data, 'vibration')
        if result:
            self.sensor_data['vibration'] = result
            self.received['vibration'] = True

    def load_cb(self, msg):
        result = self.parse(msg.data, 'load')
        if result:
            self.sensor_data['load'] = result
            self.received['load'] = True

    # ── decision logic ────────────────────────────────────────────────────────

    def evaluate(self):
        # warn if any sensor has not sent data yet
        missing = [s for s, ok in self.received.items() if not ok]
        if missing:
            self.get_logger().warn(f'waiting for first message from: {missing}')

        temp_val,  temp_state  = self.sensor_data['temperature']
        vib_val,   vib_state   = self.sensor_data['vibration']
        load_val,  load_state  = self.sensor_data['load']

        # step 1: count abnormal sensors
        abnormal_count = sum(
            1 for _, state in self.sensor_data.values() if state == 'abnormal'
        )

        # step 2: ML prediction using real sensor values
        features = np.array([[temp_val, vib_val, load_val]])
        ml_code  = int(self.model.predict(features)[0])
        ml_label = ML_LABELS[ml_code]

        # step 3: hybrid decision
        if abnormal_count >= 2:
            candidate = 'STOP SYSTEM'
        elif abnormal_count == 1:
            candidate = 'WARNING'
        else:
            # all sensors normal → trust ML output directly
            candidate = ml_label

        # step 4: stability filter
        if candidate == self.last_candidate:
            self.counter += 1
        else:
            self.counter = 1
            self.last_candidate = candidate

        if self.counter >= STABILITY_THRESHOLD:
            self.current_state = candidate

        # publish confirmed state
        out = String()
        out.data = self.current_state
        self.pub.publish(out)

        # structured log
        self.get_logger().info(
            f'\n'
            f'  Sensors:        TEMP={temp_val:.1f}({"N" if temp_state == "normal" else "A"}) '
            f'VIB={vib_val:.2f}({"N" if vib_state == "normal" else "A"}) '
            f'LOAD={load_val:.2f}({"N" if load_state == "normal" else "A"})\n'
            f'  Abnormal count: {abnormal_count}\n'
            f'  ML output:      {ml_label}\n'
            f'  Candidate:      {candidate} ({self.counter}/{STABILITY_THRESHOLD})\n'
            f'  Final decision: {self.current_state}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = MonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
