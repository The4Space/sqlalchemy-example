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
                if parse_list[1] == "好感度" or parse_list[1] == "親密度":
                    target_list = db.query(WCFavorability).all()
                    for target_row in target_list:
                        target_info = "{name} 親密度: {score}".format(
                            name=target_row.name, score=target_row.score)
                        self.message = "\n".join(target_info)
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
                self.message = "添加好感度成功~"
        except Exception as e:
            db.rollback()
            raise Exception(e)
        finally:
            db.close()

        return self.message


    def is_weichen(self, name):
        if name == "weichen" or name == "wc":
            return True

        return False


process = Process()
