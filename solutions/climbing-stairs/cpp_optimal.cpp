class Solution {
public:
    int climbStairs(int n) {
        int a = 1, b = 1;              // ways to reach step i-1 and step i
        for (int i = 2; i <= n; i++) {
            int next = a + b;
            a = b;
            b = next;
        }
        return b;
    }
};
