import dataclasses


@dataclasses.dataclass
class UsersEndPoints:
    SignUp = "/api/v1/sign_up"
    Login = "/api/v1/login"
    Delete = "/api/v1/user_delete"
    Update = "/api/v1/user_update"


@dataclasses.dataclass
class CardsEndPoints:
    CreateCard = "/api/v1/create_card"
    GetAllCard = "/api/v1/get_all_card"
    DeleteCard = "/api/v1/delete_card/{card_id}"
    GetAllGroup = "/api/v1/get_all_groups"
    GetCardFile = "/api/v1/get_card_file/{card_id}"
    GetCardInfo = "/api/v1/get_card_info/{card_id}"
    GetFavoritesCard = "/api/v1/get_favorites_cards"
    GetGroupCards = "/api/v1/get_group_cards/{group}"
    UpdateCard = "/api/v1/update_card/{card_id}"
