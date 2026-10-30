class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        idx = {}
        for i, n in enumerate(nums):
            idx[n] = i
        for i, n in enumerate(nums):
            j = idx.get(target - n)
            if j is not None and j != i:
                return [i, j]
        return []
