package com.appspot.pistatium.utilities;


import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;

/**
* = PrefList =
*   for Preferences class
*  
*/

public enum Pref{
	
	IS_FIRST_LAUNCH("is_first_launch", true), 
	
	; // 
	private final String keyName;
	private final String defaultValue;
	private final int defaultValueInt;
	private final boolean defaultValueBool;
	
	private static String PREF_NAME = "apppref";

	private Pref(String keyName, String defaultValue){
		this.keyName = keyName;
		this.defaultValue = defaultValue;
		this.defaultValueBool = false;
		this.defaultValueInt = 0;
	}
	private Pref(String keyName, int defaultValue){
		this.keyName = keyName;
		this.defaultValueInt = defaultValue;
		this.defaultValueBool = false;
		this.defaultValue = "";
	}
	private Pref(String keyName, boolean defaultValue){
		this.keyName = keyName;
		this.defaultValueBool = defaultValue;
		this.defaultValue = "";
		this.defaultValueInt = 0;
	}
	
	public String getString(Context context){
		SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
		String value = sp.getString(this.keyName, defaultValue);
		L.d("loadPref", "load key  = " + this.keyName + "; load value= " + value);
		return value;
	}
	
	public int getInt(Context context){
		SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
		int value = sp.getInt(this.keyName, defaultValueInt);
		L.d("loadPref", "load key  = " + this.keyName + "; load value= " + value);
		return value;
	}
	public boolean getBool(Context context){
		SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
		boolean value = sp.getBoolean(this.keyName, defaultValueBool);
		L.d("loadPref", "load key  = " + this.keyName + "; load value= " + value);
		return value;
	}
	
	public boolean set(Context context, String setValue){
		SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
		boolean success = sp.edit().putString(this.keyName, setValue).commit();
		L.d("savedPref","save key  = " + this.keyName + "; save value= " + setValue);
		L.d("savedPref","is_success="  + success );
		return success;
	}
	public boolean set(Context context, int setValue){
		SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
		boolean success = sp.edit().putInt(this.keyName, setValue).commit();
		L.d("savedPref","save key  = " + this.keyName + "; save value= " + setValue);
		L.d("savedPref","is_success="  + success );
		return success;
	}
	public boolean set(Context context, boolean setValue){
		SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(context);
		boolean success = sp.edit().putBoolean(this.keyName, setValue).commit();
		L.d("savedPref","save key  = " + this.keyName + "; save value= " + setValue);
		L.d("savedPref","is_success="  + success );
		return success;
	}
}