from resources.lib import ADDON_NAME
from resources.lib.gui.gui_utils import colorize, bold, notification, get_string
from resources.lib.gui.select import Select


def add_all_staged_seasons_to_library(self, showtitle):
    """Add all episodes from specified show to library."""
    # TODO: add to strings.po >
    STR_ADDING_ALL_x_SEASONS = "Adding all %s seasons..."
    STR_ALL_x_SEASONS_ADDED = "All %s seasons added"
    # <
    staged_seasons = list(
            self.database.get_season_items(status="staged", showtitle=showtitle)
    )
    self.progress_dialog.create_progress_dialog(
            msg=STR_ADDING_ALL_x_SEASONS % showtitle
    )
    for index, item in enumerate(staged_seasons):
        self.progress_dialog.update_progress_dialog(
                index / len(staged_seasons),
                f"{colorize(bold(item.showtitle()))}\n{item.episode_title_with_id()}",
        )
        item.add_to_library()
    self.progress_dialog.close_progress_dialog()
    notification(STR_ALL_x_SEASONS_ADDED % colorize(bold(showtitle), "skyblue"))


# TODO: this method need update to follow dict style

def view_seasons(self, showtitle):
    """Display all staged seasons in the specified show, which are selectable and lead to options."""
    STR_STAGED_x_SEASONS = get_string(32176)
    STR_NO_STAGED_x_SEASONS = get_string(32170)
    OPTIONS = {
        32177: self.add_all_staged_seasons_to_library,
        32171: self.remove_all_seasons,
        32068: self.remove_and_block_show,
    }
    staged_seasons = list(
            self.database.get_season_items(status="staged", showtitle=showtitle)
    )
    sel = Select(
            heading=f"{ADDON_NAME} - {STR_STAGED_x_SEASONS % colorize(bold(showtitle), 'skyblue')}",
            back_option=True,
    )
    sel.options([f"Season {x}" for x in {x.season() for x in staged_seasons}])
    sel.extra_options(list(map(get_string, OPTIONS)))
    if not staged_seasons:
        xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_STAGED_x_SEASONS % colorize(bold(showtitle), "skyblue"),
        )
        self.show()
        return
    selection = sel.show(use_details=False, pre_select=False)
    if selection:
        if selection["type"] == "item":
            self.view_episodes(
                    showtitle, season="".join(filter(str.isdigit, selection["str"]))
            )
        elif selection["type"] == "opt":
            command = OPTIONS[list(OPTIONS.keys())[selection["index1"]]]
            command(showtitle)
    self.show()


def remove_all_seasons(self, showtitle):
    """Remove all seasons from the specified show."""
    STR_REMOVING_ALL_x_SEASONS = get_string(32032) % showtitle
    STR_ALL_x_SEASONS_REMOVED = get_string(32033) % showtitle
    self.progress_dialog.create_progress_dialog(msg=STR_REMOVING_ALL_x_SEASONS)
    self.database.delete_item_from_table_with_status_or_showtitle(
            content_type="tvshow", status="staged", showtitle=showtitle
    )
    self.progress_dialog.close_progress_dialog()
    notification(STR_ALL_x_SEASONS_REMOVED)
