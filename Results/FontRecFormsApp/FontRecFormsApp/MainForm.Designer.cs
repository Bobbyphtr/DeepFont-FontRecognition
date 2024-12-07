namespace FontRecFormsApp
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.inputImageBox = new System.Windows.Forms.PictureBox();
            this.ScanButton = new System.Windows.Forms.Button();
            this.OpenFileButton = new System.Windows.Forms.Button();
            this.CropButton = new System.Windows.Forms.Button();
            this.ClearButton = new System.Windows.Forms.Button();
            this.HelpLabel = new System.Windows.Forms.Label();
            this.colorDialog1 = new System.Windows.Forms.ColorDialog();
            ((System.ComponentModel.ISupportInitialize)(this.inputImageBox)).BeginInit();
            this.SuspendLayout();
            // 
            // inputImageBox
            // 
            this.inputImageBox.BackColor = System.Drawing.Color.Transparent;
            this.inputImageBox.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Zoom;
            this.inputImageBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.inputImageBox.InitialImage = ((System.Drawing.Image)(resources.GetObject("inputImageBox.InitialImage")));
            this.inputImageBox.Location = new System.Drawing.Point(12, 53);
            this.inputImageBox.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.inputImageBox.Name = "inputImageBox";
            this.inputImageBox.Size = new System.Drawing.Size(776, 341);
            this.inputImageBox.TabIndex = 0;
            this.inputImageBox.TabStop = false;
            this.inputImageBox.DragDrop += new System.Windows.Forms.DragEventHandler(this.inputImageBox_DragDrop);
            this.inputImageBox.DragEnter += new System.Windows.Forms.DragEventHandler(this.inputImageBox_DragEnter);
            // 
            // ScanButton
            // 
            this.ScanButton.Enabled = false;
            this.ScanButton.Location = new System.Drawing.Point(360, 398);
            this.ScanButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.ScanButton.Name = "ScanButton";
            this.ScanButton.Size = new System.Drawing.Size(75, 41);
            this.ScanButton.TabIndex = 1;
            this.ScanButton.Text = "Scan";
            this.ScanButton.UseVisualStyleBackColor = true;
            this.ScanButton.Click += new System.EventHandler(this.ScanButton_Click);
            // 
            // OpenFileButton
            // 
            this.OpenFileButton.Location = new System.Drawing.Point(12, 12);
            this.OpenFileButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.OpenFileButton.Name = "OpenFileButton";
            this.OpenFileButton.Size = new System.Drawing.Size(75, 36);
            this.OpenFileButton.TabIndex = 2;
            this.OpenFileButton.Text = "Open";
            this.OpenFileButton.UseVisualStyleBackColor = true;
            this.OpenFileButton.Click += new System.EventHandler(this.OpenFile_Click);
            // 
            // CropButton
            // 
            this.CropButton.Enabled = false;
            this.CropButton.Location = new System.Drawing.Point(632, 11);
            this.CropButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.CropButton.Name = "CropButton";
            this.CropButton.Size = new System.Drawing.Size(75, 36);
            this.CropButton.TabIndex = 3;
            this.CropButton.Text = "Crop";
            this.CropButton.UseVisualStyleBackColor = true;
            this.CropButton.Click += new System.EventHandler(this.CropButton_Click);
            // 
            // ClearButton
            // 
            this.ClearButton.Enabled = false;
            this.ClearButton.Location = new System.Drawing.Point(713, 11);
            this.ClearButton.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.ClearButton.Name = "ClearButton";
            this.ClearButton.Size = new System.Drawing.Size(75, 36);
            this.ClearButton.TabIndex = 5;
            this.ClearButton.Text = "Clear";
            this.ClearButton.UseVisualStyleBackColor = true;
            this.ClearButton.Click += new System.EventHandler(this.ClearButton_Click);
            // 
            // HelpLabel
            // 
            this.HelpLabel.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.HelpLabel.BackColor = System.Drawing.SystemColors.Control;
            this.HelpLabel.ForeColor = System.Drawing.Color.Red;
            this.HelpLabel.Location = new System.Drawing.Point(453, 404);
            this.HelpLabel.Name = "HelpLabel";
            this.HelpLabel.Size = new System.Drawing.Size(335, 29);
            this.HelpLabel.TabIndex = 6;
            this.HelpLabel.Text = "Drag drop image into the container!";
            this.HelpLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.HelpLabel);
            this.Controls.Add(this.ClearButton);
            this.Controls.Add(this.CropButton);
            this.Controls.Add(this.OpenFileButton);
            this.Controls.Add(this.ScanButton);
            this.Controls.Add(this.inputImageBox);
            this.DoubleBuffered = true;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.Name = "MainForm";
            this.Text = "Recofont";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.inputImageBox)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.PictureBox inputImageBox;
        private System.Windows.Forms.Button ScanButton;
        private System.Windows.Forms.Button OpenFileButton;
        private System.Windows.Forms.Button CropButton;
        private System.Windows.Forms.Button ClearButton;
        private System.Windows.Forms.Label HelpLabel;
        private System.Windows.Forms.ColorDialog colorDialog1;
    }
}

