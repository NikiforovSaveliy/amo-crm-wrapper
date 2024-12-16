from amopy.enities import base


class Lead(base.BaseEntity):

    @property
    def type(self):
        return "leads"
