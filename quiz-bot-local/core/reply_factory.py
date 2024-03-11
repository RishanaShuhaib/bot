
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if not current_question_id:
        return False, "no question found."
    if not answer:
        return False, "please provide an answer."
    session[current_question_id] = answer
    session.save()
    return True, ""

def get_next_question(current_question_id):
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0], 0
    current_question_index = -1
    for i, question_tuple in enumerate(PYTHON_QUESTION_LIST):
        if question_tuple[0] == current_question_id:
            current_question_index = i
            break
    if current_question_index == -1:
        return "dummy question", -1
    if current_question_index + 1 < len(PYTHON_QUESTION_LIST):
        next_question_tuple = PYTHON_QUESTION_LIST[current_question_index + 1]
        return next_question_tuple[1], next_question_tuple[0]
    else:
        return None, None


def generate_final_response(session):
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0
    for question_id, correct_answer in PYTHON_QUESTION_LIST:
        if question_id in session:
            user_answer = session[question_id]
            if user_answer == correct_answer:
                correct_answers += 1
    score_percentage = (correct_answers / total_questions) * 100
    final_response = f"You have completed the quiz. Your score is {correct_answers}/{total_questions}, " \
                     f"which is {score_percentage:.2f}%."
    
    return final_response