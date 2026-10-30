class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2:
            return False
        closer = {"(": ")", "[": "]", "{": "}"}
        stack = []
        for c in s:
            if c in closer:
                stack.append(closer[c])
            elif not stack or stack.pop() != c:
                return False
        return not stack
