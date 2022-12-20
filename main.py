import uvicorn

from apps import (
    create_card_controller,
    get_card_controller,
    login_controller,
    sign_up_controller,
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
