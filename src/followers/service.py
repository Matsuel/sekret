from ..models.follower import Follower
from ..models.user import User
from ..users.service import check_if_user_exists, get_user_by_id
from src.models.database import SessionLocal
from sqlalchemy import insert, delete

def is_following(user_id: int, followed_id: int):
    with SessionLocal() as session:
        follower = session.query(Follower).filter(Follower.user_id == user_id, Follower.follower_id == followed_id).first()
        return True if follower else False
    

def follow_user_in_db(user_id: int, followed_id: int):
    if not check_if_user_exists(user_id) or not check_if_user_exists(followed_id):
        return None
    if user_id == followed_id:
        return None
    with SessionLocal() as session:
        result = True
        if is_following(user_id, followed_id):
            stmt = delete(Follower).where(Follower.user_id == user_id, Follower.follower_id == followed_id)
            result = False
        else:
            stmt = insert(Follower).values(user_id=user_id, follower_id=followed_id)
        session.execute(stmt)
        session.commit()
        return result
    
def get_follows_in_db(user_id: int):
    with SessionLocal() as session:
        follows = session.query(Follower.follower_id).filter(Follower.user_id == user_id).all()
        follows = [follow.follower_id for follow in follows]
        followers_infos = []
        for follow in follows:
            followers_infos.append(get_user_by_id(follow))
        return followers_infos
    
def get_followers_in_db(user_id: int):
    with SessionLocal() as session:
        followers = session.query(Follower.user_id).filter(Follower.follower_id == user_id).all()
        followers = [follower.user_id for follower in followers]
        followers_infos = []
        for follower in followers:
            followers_infos.append(get_user_by_id(follower))
        return followers_infos