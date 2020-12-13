import pandas as pd
import plotly.express as px

HIERARCHY = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]


class SpeciesList(pd.DataFrame):
    def find_hierarchy(self):

        hierarchy = []
        for col in HIERARCHY:
            if self[col].nunique() > 1:
                hierarchy.append(col)
        return hierarchy

    def show_treemap(self, hierarchy=None, return_fig=False, color=None):
        if hierarchy is None:
            hierarchy = self.find_hierarchy()

        if color is None:
            color = hierarchy[1]

        data = self[hierarchy].fillna("NONE").drop_duplicates(subset=hierarchy)

        fig = px.treemap(data, path=hierarchy, color=color)
        if return_fig:
            return fig
        else:
            fig.show()

    def show_sunburst(self, hierarchy=None, return_fig=False, color=None):

        if hierarchy is None:
            hierarchy = self.find_hierarchy()

        if color is None:
            color = hierarchy[1]

        data = self[hierarchy].fillna("NONE").drop_duplicates(subset=hierarchy)

        fig = px.sunburst(data, path=hierarchy, color=color)
        if return_fig:
            return fig
        else:
            fig.show()

    def show_distribution(self):
        pass
