from fastmcp import FastMCP
from tools.weather import idle_weather
from services.location_store import (
    save_location as save_location_to_store,
    get_location
)
from services.location_service import validate_province
import os

mcp = FastMCP(
    name="Xiaozhi Screen MCP",
    version="1.0.0"
)

@mcp.tool
def idle_screen_weather(
    address: str = "",
    save_location: bool = False,
    device_id: str = "ESP32_DEFAULT"
):
    """
    Hiển thị thời tiết trên màn hình chờ.

    address:
        Tỉnh/thành phố người dùng cung cấp.

    save_location:
        True  = lưu tỉnh này làm vị trí của thiết bị.
        False = chỉ lấy thời tiết, không thay đổi vị trí đã lưu.

    device_id:
        ID của thiết bị đang sử dụng MCP.
    """

    print("\n========== MCP idle_screen_weather ==========")
    print("DEVICE   =", repr(device_id))
    print("ADDRESS  =", repr(address))
    print("SAVE     =", repr(save_location))

    # =========================================================
    # 1. Nếu người dùng truyền địa chỉ mới
    # =========================================================

    if address and address.strip():

        print("VALIDATING LOCATION...")

        validation = validate_province(address)

        print("VALIDATION =", validation)

        # -----------------------------------------------------
        # Tỉnh không hợp lệ
        # -----------------------------------------------------

        if not validation.get("valid", False):

            print("LOCATION INVALID")

            return {
                "success": False,
                "location_valid": False,
                "need_retry": True,
                "input": address,
                "message": (
                    "Tỉnh hoặc thành phố chưa hợp lệ. "
                    "Vui lòng nhập lại đầy đủ tên tỉnh/thành phố."
                )
            }

        # -----------------------------------------------------
        # Lấy tên tỉnh chuẩn
        # -----------------------------------------------------

        province = validation["province"]

        print("VALID PROVINCE =", province)

        # -----------------------------------------------------
        # 2. Nếu yêu cầu lưu thì lưu vào MCP
        # -----------------------------------------------------

        if save_location:

            print("SAVING LOCATION...")

            saved = save_location_to_store(
                device_id,
                province
            )

            if not saved:

                return {
                    "success": False,
                    "location_valid": True,
                    "need_retry": False,
                    "province": province,
                    "message": "Không thể lưu vị trí."
                }

            print("LOCATION SAVED =", province)

        # -----------------------------------------------------
        # 3. Lấy thời tiết theo tỉnh vừa nhập
        # -----------------------------------------------------

        weather = idle_weather(
            province,
            False,
            device_id
        )

        return {
            "success": True,
            "location_valid": True,
            "location_saved": save_location,
            "province": province,
            "data": weather
        }

    # =========================================================
    # 4. Không truyền address
    #    → lấy vị trí đã lưu
    # =========================================================

    province = get_location(device_id)

    print("SAVED LOCATION =", province)

    if not province:

        return {
            "success": False,
            "location_valid": False,
            "need_retry": True,
            "message": (
                "Thiết bị chưa có vị trí. "
                "Vui lòng cho biết tỉnh hoặc thành phố."
            )
        }

    # =========================================================
    # 5. Lấy thời tiết theo vị trí đã lưu
    # =========================================================

    weather = idle_weather(
        province,
        False,
        device_id
    )

    return {
        "success": True,
        "location_valid": True,
        "location_saved": False,
        "province": province,
        "data": weather
    }

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )