import sys
sys.path.append(".")
from src.text_processor import text_processor
from src.text_processor import extended_is_stop

def test_text_processor():
    bug_data = "Crashes on Highscreen Zeus 1. When BarcodeScanner runs, it dead with NullPointerException 2. 3. V/CameraManager( 2138): Calculated framing rect: Rect(50, 0 - 350, 240) W/dalvikvm( 2138): threadid=17: thread exiting with uncaught exception (group=0x4001da28) E/AndroidRuntime( 21awdaw38): Uncaught handler: thread Thread-9 exiting due to uncaught exception E/AndroidRuntime( 2138): java.lang.IllegalArgumentException: Unsupported picture format: 0/null E/AndroidRuntime( 2138):"

    expected_text = "crash highscreen zeu barcodescann run dead nullpointerexcept cameramanag calcul frame rect rect dalvikvm threadid thread exit uncaught group androidruntim uncaught handler thread threadbexit due uncaught androidruntim java lang illegalargumentexcept unsupport pictur format null androidruntim"

    result_text = text_processor(bug_data)

    print(result_text)

test_text_processor()