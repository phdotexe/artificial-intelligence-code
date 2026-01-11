def towerOfHanoi(n, source, dest, temp):
    if n==1:
        print(f"Move {n} from {source} to {dest}\n")
        return
    towerOfHanoi(n-1, source, temp, dest)
    print(f"Move {n} from {source} to {dest}\n")
    towerOfHanoi(n-1, temp, dest, source)

n = 3
towerOfHanoi(n, "A", "C", "B")

