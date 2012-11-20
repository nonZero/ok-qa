from okqa.user.candidates import candidate_group


def get_recipients_for_new_question(question):

    for c in candidate_group.user_set.exclude(id=question.author.id):
        if c.email:
            yield c


def get_recipients_for_new_answer(answer):

    if answer.question.author.email:
        yield answer.question.author


