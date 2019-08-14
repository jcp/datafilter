# -*- coding: utf-8 -*-


class Save:
    """
    Mixin class for generic save method.
    """

    def save(self, path: str, endofline: str = " ") -> None:
        """
        Save rows that are not flagged.
        """
        with open(path, "w", newline="") as f:
            for row in self.results():
                if not row["flagged"]:
                    f.write(f"{row['data']}{endofline}")
