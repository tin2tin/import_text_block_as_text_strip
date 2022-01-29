bl_info = {
    "name": "Text-Block as Text Strip Content",
    "author": "Tintwotin",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Sidebar > Text Strip",
    "description": "Select a text-block and paste it into the Text strip content box",
    "warning": "",
    "wiki_url": "https://github.com/tin2tin/import_text_block_as_text_strip/",
    "category": "Sequencer",
}

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import *

def texts(self, context):
    return [(text.name, text.name, "") for text in bpy.data.texts]


class SEQUENCE_OT_import_text(Operator):
    """Import strip text from Text Editor"""

    bl_label = "Import Text from Text Editor"
    bl_idname = "sequencer.import_text"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        text = bpy.data.texts[context.scene.import_text.scene_texts]
        full = ""
        for line in text.lines:
            full += line.body + "\n"
        strip = context.active_sequence_strip
        strip.text = full
        return {"FINISHED"}

class SEQUENCE_OT_import_text(Operator):
    """Import strip text from Text Editor"""

    bl_label = "Import Text from Text Editor"
    bl_idname = "sequencer.import_text"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        text = bpy.data.texts[context.scene.import_text.scene_texts]
        full = ""
        for line in text.lines:
            full += line.body + "\n"
        strip = context.active_sequence_strip
        strip.text = full
        return {"FINISHED"}

class Import_Text_Props(PropertyGroup):
    def update_text_list(self, context):
        self.script = bpy.data.texts[self.scene_texts].name
        return None

    script: StringProperty(default="", description="Browse Text to be Linked")
    scene_texts: EnumProperty(
        name="Text-Blocks",
        items=texts,
        update=update_text_list,
        description="Text-Blocks",
    )


def panel_prepend(self, context):
    strip = context.active_sequence_strip
    strip_type = strip.type
    if strip_type == "TEXT":
        scn = context.scene
        import_text = scn.import_text
        layout = self.layout
        row = layout.row(align=True)
        row.prop(import_text, "scene_texts", text="", icon="TEXT", icon_only=True)
        row.prop(import_text, "script", text="")
        row.operator(SEQUENCE_OT_import_text.bl_idname, text="", icon="PASTEDOWN")


classes = (
    Import_Text_Props,
    SEQUENCE_OT_import_text,
)


def register():
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.import_text = bpy.props.PointerProperty(type=Import_Text_Props)
    bpy.types.SEQUENCER_PT_effect.prepend(panel_prepend)


def unregister():
    bpy.types.SEQUENCER_PT_effect.remove(panel_prepend)
    for i in classes:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.import_text


if __name__ == "__main__":
    register()
