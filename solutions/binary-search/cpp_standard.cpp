class Solution {
public:
    int helper(vector<int>& a, int lo, int hi, int t) {
        if (lo > hi) return -1;
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == t) return mid;
        return a[mid] < t ? helper(a, mid + 1, hi, t) : helper(a, lo, mid - 1, t);
    }
    int search(vector<int>& nums, int target) {
        return helper(nums, 0, (int)nums.size() - 1, target);
    }
};
