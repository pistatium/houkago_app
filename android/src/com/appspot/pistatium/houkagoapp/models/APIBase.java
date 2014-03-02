package com.appspot.pistatium.houkagoapp.models;

import java.util.List;

import lombok.Data;
import lombok.Getter;
import net.vvakame.util.jsonpullparser.annotation.JsonKey;
import net.vvakame.util.jsonpullparser.annotation.JsonModel;

import com.appspot.pistatium.houkagoapp.libs.AppListRequest;
import com.appspot.pistatium.utilities.L;

@Data
@JsonModel
public class APIBase {

	@JsonKey
	int status;
	
	@JsonKey
	List<AppModel> apps;
	
	@JsonKey
	AppModel app;

	@JsonKey
	DeveloperModel developer;
}