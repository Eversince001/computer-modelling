import bubbleSort as bSort

def SortingTask(array):
    bsort = array.copy()
    print("Default array = " + array.__str__())
    array.sort()
    print("Array sorted by default sort = " + array.__str__())
    bSort.bubbleSort(bsort)
    print("Array sorted by bubble sort = " + bsort.__str__())