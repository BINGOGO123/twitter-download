from .common_parser import CommonParser

class MediaParser(CommonParser):
    def get_entries_from_instructions(self, instructions: list) -> list:
        all_entries = []
        for instruction in instructions:
            if not isinstance(instruction, dict):
                continue
            entries = instruction.get("entries", [])
            all_entries += entries
            module_items = instruction.get("moduleItems", [])
            all_entries += module_items
        return all_entries
