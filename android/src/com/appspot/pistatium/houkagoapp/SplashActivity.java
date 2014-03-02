package com.appspot.pistatium.houkagoapp;

import android.content.Intent;
import android.os.Bundle;

import com.appspot.pistatium.houkagoapp.base.ActivityBase;
import com.appspot.pistatium.utilities.L;
import com.appspot.pistatium.utilities.Pref;

public class SplashActivity extends ActivityBase{
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		
		if(Pref.IS_FIRST_LAUNCH.getBool(getApplicationContext())) {
			onFirstLaunch();
			Pref.IS_FIRST_LAUNCH.set(getApplicationContext(), false);
		}
		Intent main = new Intent(getApplication(), MainActivity_.class);
		onLaunch(main);
		startActivity(main);
		finish();
	}



	private void onLaunch(Intent main){
		
		checkIntentFilter(main);
	}
	
	private void checkIntentFilter(Intent main){
		Intent intent = getIntent();
		String action = intent.getAction();
		if (Intent.ACTION_SEND.equals(action)) {
		  Bundle extras = intent.getExtras();
		  if (extras != null) {
		    CharSequence ext = extras.getCharSequence(Intent.EXTRA_TEXT);
		      if (ext != null) {
		    	 L.d((String) ext);
		    	 
		    	 main.putExtra("fromShareInput", ext);

		      }
		  }
		}
	}
	
	private void onFirstLaunch(){
	
	}
}
