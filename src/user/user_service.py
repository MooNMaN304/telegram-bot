from src.user.user_repository import UserRepository
from src.user.user_schema import UserSchema

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_or_update_user(self, telegram_user) -> UserSchema:
        """Создает или обновляет пользователя"""
        user_dict = {
            'telegram_id': str(telegram_user.id),
            'username': telegram_user.username,
            'first_name': telegram_user.first_name,
            'last_name': telegram_user.last_name
        }
        
        existing_user = self.user_repo.get_by_telegram_id(str(telegram_user.id))
        
        if existing_user:
            updated_user = self.user_repo.update(str(telegram_user.id), user_dict)
            return UserSchema.model_validate(updated_user)
        else:
            new_user = self.user_repo.create(user_dict)
            return UserSchema.model_validate(new_user)