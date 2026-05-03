import matplotlib.pyplot as plt

methods = ['Rule-Based', 'ML-Based', 'Hybrid']
accuracy = [78, 85, 92]

plt.figure()

plt.bar(methods, accuracy)

plt.xlabel("Method")
plt.ylabel("Accuracy (%)")
plt.title("Performance Comparison of Monitoring Approaches")

plt.ylim(0, 100)

for i, v in enumerate(accuracy):
    plt.text(i, v + 1, str(v) + "%", ha='center')

plt.show()
