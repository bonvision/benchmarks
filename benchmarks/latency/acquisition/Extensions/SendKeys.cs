using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using System.Runtime.InteropServices;

static class Keyboard
{    
    [DllImport("user32.dll", SetLastError = true)]
    static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);

    public const int KEYEVENTF_KEYDOWN = 0x0000; // New definition
    public const int KEYEVENTF_KEYUP = 0x0002; //Key up flag

    public static void SendKeyDown(int vk)
    {
        keybd_event((byte)vk, 0, KEYEVENTF_KEYDOWN, 0);
    }

    public static void SendKeyUp(int vk)
    {
        keybd_event((byte)vk, 0, KEYEVENTF_KEYUP, 0);
    }
}

[Combinator]
[Description("Sends virtual keystrokes to the operating system.")]
[WorkflowElementCategory(ElementCategory.Sink)]
public class SendKeyDown
{
    public int KeyCode { get; set; }

    public IObservable<TSource> Process<TSource>(IObservable<TSource> source)
    {
        return source.Do(value => Keyboard.SendKeyDown(KeyCode));
    }
}

[Combinator]
[Description("Sends virtual keystrokes to the operating system.")]
[WorkflowElementCategory(ElementCategory.Sink)]
public class SendKeyUp
{
    public int KeyCode { get; set; }

    public IObservable<TSource> Process<TSource>(IObservable<TSource> source)
    {
        return source.Do(value => Keyboard.SendKeyUp(KeyCode));
    }
}
