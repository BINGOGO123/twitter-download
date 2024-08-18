from .common_gallary import CommonGallary


class SinglePageGallary(CommonGallary):
    def get_dir_path_list(self, source_dir_list: list[str]) -> list[str]:
        return source_dir_list