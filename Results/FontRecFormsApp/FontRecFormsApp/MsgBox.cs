using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Text;
using System.Windows.Forms;

namespace FontRecFormsApp
{
    public partial class MsgBox : Form
    {
        public MsgBox()
        {
            InitializeComponent();
        }

        public static MsgBox msgBox; static DialogResult result = DialogResult.OK;
        
        public static DialogResult Show(string[] fontNames, Image inputImage, string[] fontFiles)
        {
            // int prediction_max_num = 5;
            
            msgBox = new MsgBox();
            msgBox.inputPictureBox.Image = inputImage;
            msgBox.top_prediction_label.Text = "Top Predictions";

            // Loading the listbox
            ListBox resultListBox = msgBox.resultListBox;
            resultListBox.DrawMode = DrawMode.OwnerDrawFixed;
            resultListBox.ItemHeight = 80;
            var dataset = new List<Tuple<string, string>>(); //fontnames, fontfiles
            for(int i = 0; i < fontNames.Length ;i++)
            {
                dataset.Add(new Tuple<string, string>(fontNames[i], fontFiles[i]));
            }
            resultListBox.DataSource = dataset;
            msgBox.ShowDialog();
            return result;
        }

        private void CustomMsgBox_Load(object sender, EventArgs e)
        {

        }

        private void resultListBox_DrawItem(object sender, DrawItemEventArgs e)
        {
            Brush roomsBrush;
            if ((e.State & DrawItemState.Selected) == DrawItemState.Selected)
            {
                e = new DrawItemEventArgs(e.Graphics, e.Font, e.Bounds,
                e.Index, e.State ^ DrawItemState.Selected, e.ForeColor, SystemColors.Control);
                roomsBrush = Brushes.Black;
            }
            else
            {
                roomsBrush = Brushes.Gray;
            }
            // Draw border line
            var linePen = new Pen(SystemBrushes.Control);
            var lineStart = new Point(e.Bounds.Left, e.Bounds.Bottom);
            var lineEnd = new Point(e.Bounds.Right, e.Bounds.Bottom);
            e.Graphics.DrawLine(linePen, lineStart, lineEnd);
            // Getting the data
            var dataItem = resultListBox.Items[e.Index] as Tuple<string, string>; // fontnames, fontfiles
            PrivateFontCollection pfc = new PrivateFontCollection();
            string base_dir = System.AppDomain.CurrentDomain.BaseDirectory;
            string lower_template = "a quick brown fox jumps over the lazy dog";
            string upper_template = "A QUICK BROWN FOX JUMPS OVER THE LAZY DOG";
            pfc.AddFontFile(base_dir + "\\Fonts_500\\" + dataItem.Item2.Trim());
            e.Graphics.DrawString(dataItem.Item1, new Font(pfc.Families[0], 18), Brushes.Black, e.Bounds.Left + 3, e.Bounds.Top + 5);
            e.Graphics.DrawString(upper_template, new Font(pfc.Families[0], 12), Brushes.Black, e.Bounds.Left + 3, e.Bounds.Top + 32);
            e.Graphics.DrawString(lower_template, new Font(pfc.Families[0], 12), Brushes.Black, e.Bounds.Left + 3, e.Bounds.Top + 56);
        }
    }
}
