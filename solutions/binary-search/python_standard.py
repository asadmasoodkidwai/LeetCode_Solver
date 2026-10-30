class Solution:
    def search(self, nums: List[int], target: int) -> int:
        def helper(lo, hi):
            if lo > hi:
                return -1
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            return helper(mid + 1, hi) if nums[mid] < target else helper(lo, mid - 1)
        return helper(0, len(nums) - 1)
