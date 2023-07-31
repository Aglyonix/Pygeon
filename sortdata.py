class SortData:

    #______________________________________________________________ Specials Variables ______________________________________________________________#

    def __init__(self, list_=[], methode='quick') -> None:
        self.list = list_
        self.methode = 'quick'

    #______________________________________________________________ Specials Functions ______________________________________________________________#
    def sort(self) -> list:
        if self.methode == 'quick':
            return self.quick_sort(self.list)
        elif self.methode == 'fusion':
            return self.sort_fusion(self.list)
        elif self.methode == 'byinser':
            return self.sort_byinsertion(self.list)

    def quick_sort(self, List: list) -> list:
        n = len(List)
        if n <= 1:
            return List
        else:
            pivot = List.pop()

        items_greater = []
        items_lower = []

        for item in List:
            if item > pivot:
                items_greater.append(item)
            else:
                items_lower.append(item)
        return self.quick_sort(items_lower) + [pivot] + self.quick_sort(items_greater)
    
    def sort_fusion(self, List: list) -> list:
        n = len(List)
        if n <= 1:
            return List
        else:
            L1 = List[0:n//2]
            L2 = List[n//2:n]
            L1_sort = self.sort_fusion(L1)
            L2_sort = self.sort_fusion(L2)
            L_sort = L1_sort + L2_sort
            return L_sort

    def sort_byinsertion(List):
        for i in range(1, len(List)):
            k = List[i]
            j = i-1
            while j >= 0 and k < List[j]:
                List[j+1] = List[j]
                j -= 1
            List[j+1] = k
        return List

print(SortData([1, 8, 9, 4, 5, 7, 6, 3, 2]).sort())