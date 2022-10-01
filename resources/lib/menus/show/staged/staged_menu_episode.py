from resources import get_string
from resources.lib import ADDON_NAME
from resources.lib.gui.gui_utils import colorize, bold, notification
from resources.lib.gui.select import Select


def episode_options(self, item, season):
    """Provide options for a single staged episode in a dialog window."""
    STR_ADD = get_string(32048)
    STR_REMOVE = get_string(32017)
    STR_REMOVE_AND_BLOCK_EPISODE = get_string(32079)
    STR_GENERATE_METADATA_ITEM = get_string(32052)
    STR_BACK = get_string(32011)
    STR_STAGED_EPISODE_OPTIONS = get_string(32080)
    lines = [
        STR_ADD,
        STR_REMOVE,
        STR_GENERATE_METADATA_ITEM,
        STR_BACK,
    ]
    ret = xbmcgui.Dialog().select(
            f"{STR_STAGED_EPISODE_OPTIONS} - {colorize(bold(item.showtitle()), 'skyblue')} - {colorize(bold(item.episode_id()), 'green')}",
            lines,
    )
    if ret >= 0:
        if lines[ret] == STR_ADD:
            item.add_to_library()
            self.view_episodes(item.showtitle(), season)
        elif lines[ret] == STR_REMOVE:
            item.delete()
            self.view_episodes(item.showtitle(), season)
        elif lines[ret] == STR_REMOVE_AND_BLOCK_EPISODE:
            item.remove_and_block()
            self.view_episodes(item.showtitle(), season)
            self.episode_options(item, season)
        elif lines[ret] == STR_GENERATE_METADATA_ITEM:
            item.create_metadata_item()
            self.episode_options(item, season)
        elif lines[ret] == STR_BACK:
            self.view_episodes(item.showtitle(), season)
            return
        # self.view_episodes(item.showtitle(), season)


def view_episodes(self, showtitle, season):
    """Display all staged episodes in the specified show, which are selectable and lead to options."""
    STR_NO_STAGED_x_EPISODES = get_string(32065)
    STR_STAGED_x_EPISODES = get_string(32070)
    staged_episodes = list(
            self.database.get_episode_items(
                    status="staged", showtitle=showtitle, season=season
            )
    )
    OPTIONS = {
        32066: [self.add_all_staged_episodes_to_library, staged_episodes],
        32029: [self.remove_all_episodes, showtitle],
        32068: [self.remove_and_block_show, showtitle],
    }
    if not staged_episodes:
        xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_STAGED_x_EPISODES % colorize(bold(showtitle), "skyblue"),
        )
        self.show()
        return
    sel = Select(
            f"{ADDON_NAME} - {STR_STAGED_x_EPISODES % colorize(bold(showtitle), 'skyblue')}",
            back_option=True,
    )
    sel.options([str(x) for x in staged_episodes])
    sel.extra_options(OPTIONS)
    selection = sel.show(use_details=False, pre_select=False)
    if selection:
        if selection["type"] == "item":
            self.episode_options(staged_episodes[selection["index1"]], season)
        elif selection["type"] == "opt":
            command = OPTIONS[list(OPTIONS.keys())[selection["index1"]]]
            command[0](command[1])
        self.view_seasons(showtitle)


def add_all_staged_episodes_to_library(self, episodes):
    """Add all episodes from specified show to library."""
    STR_ADDING_ALL_x_EPISODES = get_string(32071)
    STR_ALL_x_EPISODES_ADDED = get_string(32072)
    showtitle = episodes[0].showtitle
    self.progress_dialog.create_progress_dialog(
            msg=STR_ADDING_ALL_x_EPISODES % showtitle
    )
    for index, item in enumerate(episodes):
        self.progress_dialog.update_progress_dialog(
                index / len(episodes),
                f"{colorize(bold(item.showtitle()))}\n{item.episode_title_with_id()}",
        )
        item.add_to_library()
    self.progress_dialog.close_progress_dialog()
    notification(STR_ALL_x_EPISODES_ADDED % colorize(bold(showtitle), "skyblue"))


def remove_all_episodes(self, showtitle):
    """Remove all episodes from the specified show."""
    formed_title = colorize(bold(showtitle), "skyblue")
    STR_REMOVING_ALL_x_EPISODES = get_string(32032) % formed_title
    STR_ALL_x_EPISODES_REMOVED = get_string(32033) % formed_title
    self.progress_dialog.create_progress_dialog(msg=STR_REMOVING_ALL_x_EPISODES)
    self.database.delete_item_from_table_with_status_or_showtitle(
            content_type="tvshow", status="staged", showtitle=showtitle
    )
    self.progress_dialog.close_progress_dialog()
    notification(STR_ALL_x_EPISODES_REMOVED)
