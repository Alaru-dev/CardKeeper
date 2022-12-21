import uvicorn

from apps import (
    create_card_controller,
    delete_card_controller,
    get_all_card_controller,
    get_all_groups_controller,
    get_card_file_controller,
    get_card_info_controller,
    get_favorites_cards,
    get_group_cards_controller,
    login_controller,
    sign_up_controller,
    update_card_controller,
    user_delete_controller,
    user_update_controller,
)
from projconf.settings import HOST, PORT

if __name__ == "__main__":
    uvicorn.run(
        "projconf.application:app",
        host=HOST,
        port=PORT,
        log_level="info",
        reload=True,
    )
