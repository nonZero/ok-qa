from okqa.qa import signals
import sending

signals.answer_posted.connect(sending.send_new_answer)
signals.question_posted.connect(sending.send_new_question)
