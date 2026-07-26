class InterviewScoringService:
    """
    Service responsible for calculating the final interview score
    using weighted evaluation metrics.
    """

    def calculate_score(
        self,
        evaluation: dict,
    ) -> dict:
        """
        Calculate the final interview score using weighted metrics.

        Weight Distribution:
        - Technical Knowledge : 50%
        - Problem Solving     : 20%
        - Explanation Quality : 15%
        - Communication       : 10%
        - Completeness        : 5%

        Args:
            evaluation: Dictionary returned by AnswerEvaluator.

        Returns:
            Dictionary containing individual metrics and the final score.
        """

        technical = float(
            evaluation.get(
                "technical_score",
                0,
            )
        )

        problem_solving = float(
            evaluation.get(
                "practical_score",
                0,
            )
        )

        explanation = float(
            evaluation.get(
                "explanation_quality",
                0,
            )
        )

        communication = float(
            evaluation.get(
                "communication_score",
                explanation,
            )
        )

        missing_concepts = evaluation.get(
            "missing_concepts",
            [],
        )

        missing_count = len(missing_concepts)

        if missing_count == 0:
            completeness = 100

        elif missing_count == 1:
            completeness = 80

        elif missing_count == 2:
            completeness = 60

        else:
            completeness = 40

        final_score = round(
            (
                technical * 0.50
                + problem_solving * 0.20
                + explanation * 0.15
                + communication * 0.10
                + completeness * 0.05
            ),
            2,
        )

        return {
            "technical_knowledge": technical,
            "problem_solving": problem_solving,
            "explanation_quality": explanation,
            "communication": communication,
            "completeness": completeness,
            "final_score": final_score,
        }