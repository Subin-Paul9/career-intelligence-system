class LearningResourceService:
    """
    Service responsible for recommending
    learning resources based on missing concepts.
    """

    RESOURCE_MAP = {

        "Python": [
            "https://docs.python.org/3/",
            "https://realpython.com/",
        ],

        "FastAPI": [
            "https://fastapi.tiangolo.com/",
        ],

        "SQL": [
            "https://www.postgresql.org/docs/",
            "https://www.w3schools.com/sql/",
        ],

        "Normalization": [
            "https://www.geeksforgeeks.org/dbms-normalization/",
        ],

        "Indexing": [
            "https://www.geeksforgeeks.org/sql-indexes-in-dbms/",
        ],

        "REST API": [
            "https://fastapi.tiangolo.com/tutorial/",
        ],

        "JWT": [
            "https://jwt.io/introduction",
        ],

        "OOP": [
            "https://realpython.com/python3-object-oriented-programming/",
        ],

        "Data Structures": [
            "https://www.geeksforgeeks.org/data-structures/",
        ],

        "Algorithms": [
            "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
        ],
    }

    def __init__(
        self,
    ):
        pass

    # =====================================================
    # Get Learning Resources
    # =====================================================

    def get_learning_resources(
        self,
        missing_concepts: list[str],
    ) -> list[str]:
        """
        Return recommended learning resources
        based on the identified missing concepts.
        """

        learning_resources = []

        for concept in missing_concepts:

            for (
                keyword,
                resources,
            ) in self.RESOURCE_MAP.items():

                if (
                    keyword.lower()
                    in concept.lower()
                ):

                    learning_resources.extend(
                        resources,
                    )

        # ---------------------------------------------
        # Remove Duplicate Resources
        # ---------------------------------------------

        unique_resources = list(
            dict.fromkeys(
                learning_resources,
            )
        )

        return unique_resources