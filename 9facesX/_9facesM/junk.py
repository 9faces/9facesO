import random
class JunkGenerator:
    @staticmethod
    def generate_inline(count=50):
        parts = []
        for k in range(count):
            parts.append(f"local _j{k}={random.randint(1,999)}{random.choice('+-*')}{random.randint(1,99)};")
        return " ".join(parts)
