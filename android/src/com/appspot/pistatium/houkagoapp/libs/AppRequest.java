package com.appspot.pistatium.houkagoapp.libs;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import lombok.Data;

import net.vvakame.util.jsonpullparser.annotation.JsonKey;
import net.vvakame.util.jsonpullparser.annotation.JsonModel;

import org.json.JSONObject;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.VolleyError;
import com.android.volley.RequestQueue.RequestFilter;
import com.android.volley.Response;
import com.android.volley.Response.ErrorListener;
import com.android.volley.Response.Listener;
import com.appspot.pistatium.houkagoapp.models.APIBase;
import com.appspot.pistatium.houkagoapp.models.APIBaseGen;
import com.appspot.pistatium.houkagoapp.models.AppModel;
import com.appspot.pistatium.utilities.L;

public class AppRequest extends Request<List<AppModel>> {

	private final Listener<List<AppModel>> mListener;
	private Map<String, String> mParams;

	public AppRequest(int method, String url, Listener<List<AppModel>> listener,
			ErrorListener errorListener) {
		super(method, url, errorListener);
		mListener = listener;
	}


	public void setParams(Map<String, String> map) {
		mParams = map;
	}

	protected Map<String, String> getParams() {
		return mParams;
	}

	protected Response<List<AppModel>> parseNetworkResponse(NetworkResponse networkResponse) {

		String resp = new String(networkResponse.data);
		
		long latest_app_id = 0;
		AppModel latest_app = AppModel.getLatestOne();
		if (latest_app != null) {
			latest_app_id = latest_app.getApp_id();
		}
		
		List<AppModel> apps = new ArrayList<AppModel>();
		try {
			APIBase api = APIBaseGen.get(resp);
			apps = api.getApps();
			for (AppModel app : apps) {
				if (app.getApp_id() == latest_app_id) {
					L.d("This app is already added");
					break;
				}
				app.save();
			}
		} catch (Exception e) {
			L.d("json error");
			return Response.error(new VolleyError());
		}
		return Response.success(apps, getCacheEntry());
	}


	@Override
	protected void deliverResponse(List<AppModel> response) {
		mListener.onResponse(response);

	}
}
