from flask import (
    Blueprint,
    Response,
    redirect,
    render_template,
    request,
    url_for,
)

from pandora.forms import DeviceSearchForm
from pandora.services import PandoraService
from pandora.utils import datetime_to_url, parse_datetime_url

pandora_page = Blueprint("pandora_page", __name__)


@pandora_page.route("/", methods=["GET"])
async def index() -> str:
    form = DeviceSearchForm()
    start_time = parse_datetime_url(request.args.get("st"))
    end_time = parse_datetime_url(request.args.get("et"))

    devices = []
    if start_time and end_time:
        devices = await PandoraService.get_decoded_payloads(
            list_id=[252, 256, 257, 264, 269, 273],
            start_time=start_time,
            end_time=end_time,
        )
    context = {
        "devices": devices,
        "form": form,
        "start_time": start_time,
        "end_time": end_time,
    }
    return render_template("index.html", **context)


@pandora_page.route("/", methods=["POST"])
def index_form() -> Response:
    form = DeviceSearchForm()
    if form.validate_on_submit():
        start_time = form.start_time.data
        end_time = form.end_time.data
        values = {
            "st": datetime_to_url(start_time),
            "et": datetime_to_url(end_time),
        }
        return redirect(url_for("pandora_page.index", **values))
