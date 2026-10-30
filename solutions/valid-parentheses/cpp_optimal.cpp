class Solution {
public:
    bool isValid(string s) {
        if (s.size() % 2) return false;
        string st;
        st.reserve(s.size());
        for (char c : s) {
            if (c == '(') st.push_back(')');
            else if (c == '[') st.push_back(']');
            else if (c == '{') st.push_back('}');
            else if (st.empty() || st.back() != c) return false;
            else st.pop_back();
        }
        return st.empty();
    }
};
