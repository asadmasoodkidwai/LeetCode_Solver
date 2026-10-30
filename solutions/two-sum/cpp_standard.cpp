class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> idx;
        for (int i = 0; i < nums.size(); i++) idx[nums[i]] = i;
        for (int i = 0; i < nums.size(); i++) {
            int need = target - nums[i];
            if (idx.count(need) && idx[need] != i) return {i, idx[need]};
        }
        return {};
    }
};
