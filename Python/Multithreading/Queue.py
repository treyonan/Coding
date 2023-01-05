import queue

q = queue.Queue()
q2 = queue.LifoQueue()
q3 = queue.PriorityQueue()

numbers = [10,20,30,40,50,60,70]
numbers2 = [1,2,3,4,5,6,7]
q3.put((2, "Hello World"))
q3.put((11, 99))
q3.put((5, 7.5))
q3.put((1, True))


for number in numbers:
    q.put(number)

print(q.get())
print(q.get())

for x in numbers2:
    q2.put(x)

print(q2.get())
print(q2.get())

while not q3.empty():
    print(q3.get())

