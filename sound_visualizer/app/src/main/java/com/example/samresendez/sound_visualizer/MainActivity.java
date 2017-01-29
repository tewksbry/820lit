package com.example.samresendez.sound_visualizer;

import android.content.Context;
import android.content.DialogInterface;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.NumberPicker;
import android.widget.SeekBar;

import com.flask.colorpicker.ColorPickerView;
import com.flask.colorpicker.OnColorSelectedListener;
import com.flask.colorpicker.builder.ColorPickerClickListener;
import com.flask.colorpicker.builder.ColorPickerDialogBuilder;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.lang.reflect.Array;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private DatabaseReference mDatabase;
    private int patternNum;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mDatabase = FirebaseDatabase.getInstance().getReference();
        SeekBar bar = (SeekBar) findViewById(R.id.brightness_bar);
        bar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                int val = (int)(i*2.55);
                mDatabase.child("brightness").setValue(val);

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
        NumberPicker binaryButton = (NumberPicker) findViewById(R.id.binaryButton);
        NumberPicker displayOne = (NumberPicker) findViewById(R.id.display_picker);

        binaryButton.setMinValue(0);
        binaryButton.setMaxValue(6);

        displayOne.setMinValue(0);
        displayOne.setMaxValue(5);


        String display_names[] = new String[6];
        display_names[0] = "Middle Out";
        display_names[1] = "Middle Out Fill";
        display_names[2] = "Strobe";
        display_names[3] = "Cycle";
        display_names[4] = "Fill";
        display_names[5] = "Middle Out White";

        String pattern_names[] = new String[7];
        pattern_names[0] = "Rainbow";
        pattern_names[1] = "Random";
        pattern_names[2] = "Bright Random";
        pattern_names[3] = "Grayscale";
        pattern_names[4] = "FIGHT ON!";
        pattern_names[5] = "Mood Lighting";
        pattern_names[6] = "Single Light";

        binaryButton.setDisplayedValues(pattern_names);
        displayOne.setDisplayedValues(display_names);

        binaryButton.setOnValueChangedListener(new NumberPicker.OnValueChangeListener() {
            @Override
            public void onValueChange(NumberPicker numberPicker, int i, int i1) {
                mDatabase.child("PatternID").setValue(i);
            }
        });
        displayOne.setOnValueChangedListener(new NumberPicker.OnValueChangeListener() {
            @Override
            public void onValueChange(NumberPicker numberPicker, int i, int i1) {
                mDatabase.child("DisplayID").setValue(i);
            }
        });
        final Button color_btn = (Button) findViewById(R.id.select_color);
        color_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final Context context = MainActivity.this;

                ColorPickerDialogBuilder
                        .with(context)
                        .setTitle("Set Light Color")
                        .initialColor(0xFFFFFFFF)
                        .wheelType(ColorPickerView.WHEEL_TYPE.FLOWER)
                        .density(12)
                        .setPositiveButton("Select", new ColorPickerClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i, Integer[] integers) {
                                Log.e("Asdf",Integer.toHexString(i));
                                mDatabase.child("Test").setValue("Hi");
                                String str = Integer.toHexString(i);
                                int W = Integer.valueOf(str.substring(0,2), 16);
                                int R = Integer.valueOf(str.substring(2,4), 16);
                                int G = Integer.valueOf(str.substring(4,6), 16);
                                int B = Integer.valueOf(str.substring(6,8), 16);
                                mDatabase.child("R").setValue(R);
                                mDatabase.child("G").setValue(G);
                                mDatabase.child("B").setValue(B);
                                Log.e("Asdf",Integer.toString(R) + " " + Integer.toString(G) + " " + Integer.toString(B));

                            }
                        })
                        .setOnColorSelectedListener(new OnColorSelectedListener() {
                            @Override
                            public void onColorSelected(int i) {
                                Log.e("Asdf","We get here!");
                                String str = Integer.toHexString(i);
                                int W = Integer.valueOf(str.substring(0,2), 16);
                                int R = Integer.valueOf(str.substring(2,4), 16);
                                int G = Integer.valueOf(str.substring(4,6), 16);
                                int B = Integer.valueOf(str.substring(6,8), 16);

                                mDatabase.child("R").setValue(R);
                                mDatabase.child("G").setValue(G);
                                mDatabase.child("B").setValue(B);


                            }
                        })
                        .showColorEdit(true)
                        .setColorEditTextColor(ContextCompat.getColor(MainActivity.this, android.R.color.holo_blue_bright))
                        .build()
                        .show();
            }
        });
        SeekBar cycle_button = (SeekBar) findViewById(R.id.cycle_bar);
        cycle_button.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {

                i = (int)(i * 2.55);
                mDatabase.child("cycleSpeed").setValue(255 - i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
        SeekBar white_bar = (SeekBar) findViewById(R.id.white_bar);
        white_bar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                mDatabase.child("W").setValue((int)(2.55*i));
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
    }

}
