package com.appspot.pistatium.houkagoapp.base;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import com.activeandroid.ActiveAndroid;
import com.appspot.pistatium.houkagoapp.SplashActivity;
import com.appspot.pistatium.utilities.L;
import com.appspot.pistatium.utilities.Pref;
import com.parse.Parse;
import com.parse.ParseAnalytics;
import com.parse.ParseInstallation;
import com.parse.PushService;

import android.content.res.AssetManager;
import android.graphics.Typeface;
import android.view.View;
import android.widget.TextView;

public class HoukagoApplication extends com.activeandroid.app.Application {

	@Override
	public void onCreate() {
		super.onCreate();

		Parse.initialize(this, "SqMIPgEkeAUJcX0MotNp44ZUsDxWoJ5PBzM0gkN7",
				"aHga8WjWMcct1GLxjtYmbIlUnlzjwJicZBWRygPU");
		ParseInstallation.getCurrentInstallation().saveInBackground();
		PushService.subscribe(this, "", SplashActivity.class);

	}

}
