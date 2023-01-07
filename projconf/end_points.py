import dataclasses


@dataclasses.dataclass
class UsersEndPoints:
    SignUp = "/api/v1/sign_up"
    Login = "/api/v1/login"
    Delete = "/api/v1/user"
    Update = "/api/v1/user"


@dataclasses.dataclass
class CardsEndPoints:
    GetAllCard = "/api/v1/cards/all"
    GetAllGroup = "/api/v1/cards/groups"
    GetGroupCards = "/api/v1/cards/{group}"
    GetFavoritesCard = "/api/v1/cards/favorite"
    CreateCard = "/api/v1/cards/create"
    GetCardFile = "/api/v1/cards/{card_id}/file"
    GetCardInfo = "/api/v1/cards/{card_id}/info"
    UpdateCardInfo = "/api/v1/cards/{card_id}/info"
    DeleteCard = "/api/v1/cards/{card_id}"
