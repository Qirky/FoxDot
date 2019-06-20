import wx.stc
import wx

class Text(wx.TextCtrl):
    """docstring for SimpleText"""
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self._default_style   = wx.TextAttr(wx.Colour(0, 0, 0), wx.Colour(255,255,255))
        self._highlight_style = wx.TextAttr(wx.Colour(255,255,255), wx.Colour(255,0,0))

    # Return values

    def get_insert(self):
        _, col, row = self.PositionToXY(self.GetInsertionPoint())
        return (row, col)

    def get_current_row(self):
        return self.get_insert()[0]

    def get_current_block(self):
        """ Returns the start and end rows of the current block """
        anchor, _ = self.get_insert()

        # Go forward
        row = anchor
        while True:
            text = self.GetLineText(row).strip()
            if len(text) == 0:
                end = row - 1
                break
            row += 1

        # Go backwards
        row = anchor
        while True:
            text = self.GetLineText(row).strip()
            if len(text) == 0:
                start = row + 1
                break
            row -= 1            
            
        return (start, end)

    def get_current_line_text(self):
        """ Returns the text from the current line """
        return self.GetLineText(self.get_insert()[0])

    def get_block_text(self, start, end):
        """ Returns the text between """
        return "\n".join([self.GetLineText(row) for row in range(start, end + 1)])

    # Highlight block

    def highlight_block(self, start, end, undo=False):
        for row in range(start, end + 1):
            if undo:
                self.de_highlight_line(row)
            else:
                self.highlight_line(row)
        return

    def highlight_line(self, row):
        start = self.XYToPosition(0, row)
        end   = self.XYToPosition(self.GetLineLength(row), row)
        self.SetStyle(start, end, self._highlight_style)
        return

    def de_highlight_line(self, row):
        start = self.XYToPosition(0, row)
        end   = self.XYToPosition(self.GetLineLength(row), row)
        val = self.SetStyle(start, end, self._default_style)
        return

    def delete_all(self):
        """ Removes all the text in the editor """
        return self.Remove(0, self.GetLastPosition())
