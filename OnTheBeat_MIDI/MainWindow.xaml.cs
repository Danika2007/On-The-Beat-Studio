using System;
using System.Text;
using System.Text.Encodings;
using System.Text.Unicode;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using NAudio.Wave;

namespace OnTheBeat_MIDI
{
    public partial class MainWindow : Window
    {
        private WaveOutEvent outputDevice;
        private AudioFileReader audioFile;

        public MainWindow()
        {
            InitializeComponent();
            this.Focus(); 
        }

        private void PlayNote(string note)
        {
            string projectDir = @"C:\Users\szabad.daniel\source\repos\OnTheBeat_MIDI\Assets";
            string soundPath = System.IO.Path.Combine(projectDir, $"{note}.wav");

            if (System.IO.File.Exists(soundPath))
            {
                audioFile?.Dispose();
                audioFile = new AudioFileReader(soundPath);
                outputDevice = new WaveOutEvent();
                outputDevice.Init(audioFile);
                outputDevice.Play();
            }
            else
            {
                MessageBox.Show($"A '{note}.wav' fájl nem található!");
            }
        }

        private void Window_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
        {
            switch (e.Key)
            {
                case System.Windows.Input.Key.A:
                    PlayNote("C");
                    StatusText.Text = "A3 hang szól";
                    break;
                case System.Windows.Input.Key.S:
                    PlayNote("D");
                    StatusText.Text = "B3 hang szól";
                    break;
                case System.Windows.Input.Key.D:
                    PlayNote("E");
                    StatusText.Text = "C3 hang szól";
                    break;
                case System.Windows.Input.Key.F:
                    PlayNote("F");
                    StatusText.Text = "D3 hang szól";
                    break;
                case System.Windows.Input.Key.G:
                    PlayNote("G");
                    StatusText.Text = "E3 hang szól";
                    break;
                case System.Windows.Input.Key.H:
                    PlayNote("A4");
                    StatusText.Text = "A4 hang szól";
                    break;
                case System.Windows.Input.Key.J:
                    PlayNote("B4");
                    StatusText.Text = "B4 hang szól";
                    break;
                case System.Windows.Input.Key.K:
                    PlayNote("C4");
                    StatusText.Text = "C4 hang szól";
                    break;
                case System.Windows.Input.Key.L:
                    PlayNote("D4");
                    StatusText.Text = "D4 hang szól";
                    break;
                
                default:
                    StatusText.Text = "Ismeretlen billentyű";
                    break;
            }
        }
    }
}