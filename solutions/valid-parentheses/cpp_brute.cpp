class Solution {
public:
    bool isValid(string s) {
        // repeatedly strip matched pairs until nothing changes
        bool changed = true;
        while (changed) {
            changed = false;
            for (const string& p : {"()", "[]", "{}"}) {
                size_t pos;
                while ((pos = s.find(p)) != string::npos) {
                    s.erase(pos, 2);
                    changed = true;
                }
            }
        }
        return s.empty();
    }
};
