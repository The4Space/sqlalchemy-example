# coding=utf-8
import operator

from database.config import db
from database.model.kks_undercover import WCFavorability

class Process:
    def __init__(self):
        self.message = ""

    def controller(self, request_data):
        parse_list = request_data.split(" ")
        try:
            if self.is_weichen(parse_list[0]):
                if parse_list[1] == u"favor" or parse_list[1] == u"favorlist":
                    target_list = db.query(WCFavorability).all()
                    target_info = []
                    for target_row in target_list:
                        target_info.append(u"{name} 親密度: {score} {heart}".format(
                            name=target_row.name,
                            score=target_row.score,
                            heart=self.get_heart(target_row.score)))
                    self.message = u"\n".join(target_info)
            else:
                ops = {"+": operator.add, "-": operator.sub}
                target_name = parse_list[0]
                db_data = db.query(WCFavorability).filter(
                    WCFavorability.name==target_name).one_or_none()
                if db_data is None:
                    score = ops[parse_list[1][0]](0, int(parse_list[1][1:]))
                    insert_data = WCFavorability(
                        name=target_name, nick_name="", score=score)
                    db.add(insert_data)
                    db.commit()
                else:
                    score = ops[parse_list[1][0]](int(db_data.score), int(parse_list[1][1:]))
                    update_data = {"score": score}
                    db.query(WCFavorability).filter(WCFavorability.name==target_name).update(update_data)
                    db.commit()
                self.message = u"添加好感度成功~"
        except Exception as e:
            db.rollback()
            print e
            raise Exception(e)
        finally:
            db.close()
        return self.message

    def get_heart(self, score):
        if score < 0:
            heart_str = ":poop:"
        elif 0 < score <= 10:
            heart_str = ":heart:"
        elif 10 <= score <= 30:
            heart_str = ":heart::heart:"
        elif 30 <= score <= 50:
            heart_str = ":heart::heart::heart:"
        elif 50 <= score <= 70:
            heart_str = ":heart::heart::heart::heart:"
        else:
            heart_str = ":heart::heart::heart::heart::heart:"

        return heart_str

    def is_weichen(self, name):
        if name == "weichen" or name == "wc":
            return True

        return False


process = Process()
