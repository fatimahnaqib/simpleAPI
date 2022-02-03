
"""
Calculates the average score 

"""
def calc_average_score(student_scores):
    total_score = 0
    if len(student_scores) == 0:
        return 0
    for student_score in student_scores:
        total_score += float(student_score.score)
    print(total_score)
    return total_score / len(student_scores)