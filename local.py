from src.incbl import incbl

if __name__ = "__main__":

    # TODO: argparse to add parameters
    incbl = incbl(bug_reports_path, code_base_path)
    incbl.index_update()
    incbl.idf_update()
    incbl.localization()
    incbl.evaluation()
    incbl.fixed_bugs_update()


