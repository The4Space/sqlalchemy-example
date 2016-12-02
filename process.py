# coding=utf-8
import operator

from database.config import db
from database.model.kks_undercover import WCFavorability


class Process:
    def __init__(self):
        self.return_message = ""

    def set_return_message(self, target_list):
        target_info = []
        for target_row in target_list:
            target_info.append(
                u"{name} 親密度: {score} {heart}".format(
                    name=target_row.name,
                    score=target_row.score,
                    heart=self.get_heart(target_row.score)
                )
            )
        self.return_message = u"\n".join(target_info)

    def controller(self, request_data):
        parse_list = request_data.split(" ")
        try:
            if self.is_weichen(parse_list[0]):
                if parse_list[1] == u"好感度" or parse_list[1] == u"親密度":
                    target_list = db.query(WCFavorability).all()
                    self.set_return_message(target_list)
            else:
                ops = {"+": operator.add, "-": operator.sub}
                target_name = parse_list[0]
                db_data = db.query(WCFavorability).filter(
                    WCFavorability.name == target_name).one_or_none()
                if db_data is None:
                    score = ops[parse_list[1][0]](0, int(parse_list[1][1:]))
                    insert_data = WCFavorability(name=target_name, score=score)
                    db.add(insert_data)
                    db.commit()
                else:
                    score = ops[parse_list[1][0]](int(db_data.score), int(parse_list[1][1:]))
                    update_data = {"score": score}
                    db.query(WCFavorability).filter(WCFavorability.name == target_name).update(
                        update_data)
                    db.commit()
                target_list = db.execute("SELECT * FROM wc_favorability")
                print target_list
                self.return_message = self.set_return_message(target_list)
        except Exception as e:
            db.rollback()
            print e
            raise Exception(e)
        finally:
            db.close()
        return self.return_message

    def get_heart(self, score):
        if score < 0:
            heart_str = ":poop:"
        elif 0 < score <= 10:
            heart_str = ":heart:"
        elif 10 <= score <= 30:
            heart_str = ":heart:" * 2
        elif 30 <= score <= 50:
            heart_str = ":heart:" * 3
        elif 50 <= score <= 70:
            heart_str = ":heart:" * 4
        else:
            heart_str = ":heart:" * 5

        return heart_str

    def is_weichen(self, name):
        if name == "weichen" or name == "wc":
            return True

        return False


process = Process()
