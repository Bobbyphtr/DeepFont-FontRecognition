using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FontRecFormsApp
{
    public partial class LoadingBox : Form
    {
        public LoadingBox()
        {
            InitializeComponent();
        }

        public static LoadingBox loadingBox; static DialogResult result = DialogResult.OK;

        public static DialogResult Show()
        {
            loadingBox = new LoadingBox();
            loadingBox.ShowDialog();
            return result;
        }

        public static Boolean Dismiss()
        {
            if (loadingBox.InvokeRequired)
            {
                loadingBox.Invoke(new MethodInvoker(delegate { loadingBox.Close(); }));
            }else
            {
                loadingBox.Close();
            }
            
            return true;
        }
    }
}
