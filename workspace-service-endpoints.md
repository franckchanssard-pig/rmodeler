# WorkspaceService v1 endpoints by tag

Auth: Bearer (JWT)


## AccessRights

- `DELETE` `/api/workspace/accessrights/RemoveAccessRightMetric/{applicationId}`
- `GET` `/api/workspace/accessrights/ExposeAccessRightsSchema`
- `GET` `/api/workspace/accessrights/List/{applicationId}`
- `POST` `/api/workspace/accessrights/AddAccessRightMetric/{applicationId}`
- `POST` `/api/workspace/accessrights/AddAccessRightMetricForListProperties/{applicationId}`
- `POST` `/api/workspace/accessrights/AddAccessRightMetricForMetrics/{applicationId}`
- `POST` `/api/workspace/accessrights/FindSome/{applicationId}`
- `POST` `/api/workspace/accessrights/GetReadAccessRightsDetails/{applicationId}`
- `PUT` `/api/workspace/accessrights/BatchUpdateAccessRightMetric/{applicationId}`
- `PUT` `/api/workspace/accessrights/UpdateAccessRightMetric/{applicationId}`

## AccessRightsInternal

- `GET` `/api/workspace/internals/accessrights/DeleteOrphanArmSets/{organizationId}`
- `GET` `/api/workspace/internals/accessrights/GetAccessRightsMetricsConfigurationByEntity/{organizationId}/{applicationId}/{scenarioId}`
- `GET` `/api/workspace/internals/accessrights/GetArmSetCardinality`
- `GET` `/api/workspace/internals/accessrights/GetArmSetExpandedFormula`
- `GET` `/api/workspace/internals/accessrights/GetArmSetWithReferences`
- `GET` `/api/workspace/internals/accessrights/GetArmSetsStatistics`
- `GET` `/api/workspace/internals/accessrights/GetListAccessRightsInfo/{applicationId}/{listId}`
- `GET` `/api/workspace/internals/accessrights/GetMetricAccessRightsInfo/{applicationId}/{metricId}`
- `GET` `/api/workspace/internals/accessrights/List/{applicationId}`
- `GET` `/api/workspace/internals/accessrights/ListOrphanArmSets/{organizationId}`
- `GET` `/api/workspace/internals/accessrights/ListStaleArmSetHandles/{organizationId}`
- `GET` `/api/workspace/internals/accessrights/QueryArmSets`
- `GET` `/api/workspace/internals/accessrights/QueryDetailedArmSets`
- `POST` `/api/workspace/internals/accessrights/CompareArmSets/{applicationId}`
- `POST` `/api/workspace/internals/accessrights/PreviewArmSet/{applicationId}`
- `POST` `/api/workspace/internals/accessrights/RunCompareArmSetsPatchOnApplication/{applicationId}`
- `POST` `/api/workspace/internals/accessrights/StartAccessRightsViewBench/{organizationId}/{viewAsUserId}`
- `POST` `/api/workspace/internals/accessrights/SwitchAccessRightsMode/{organizationId}`
- `PUT` `/api/workspace/internals/accessrights/BumpAccessRightVersion`
- `PUT` `/api/workspace/internals/accessrights/CopyMultipleUserSecuritiesInSnapshot`
- `PUT` `/api/workspace/internals/accessrights/RegenerateAccessRights`

## AnalyticsInternal

- `GET` `/api/workspace/internals/analytics/GetLastExport`
- `POST` `/api/workspace/internals/analytics/Export`
- `POST` `/api/workspace/internals/analytics/RepairLastFailedExport`

## Application

- `DELETE` `/api/workspace/application/Remove/{applicationId}`
- `GET` `/api/workspace/application/All/{organizationId}`
- `GET` `/api/workspace/application/AllPermissions/{organizationId}`
- `GET` `/api/workspace/application/ExposePermissionsSchema`
- `GET` `/api/workspace/application/Get/{applicationId}`
- `GET` `/api/workspace/application/GetPermission/{applicationId}`
- `GET` `/api/workspace/application/ListApplicationLibraries/{applicationId}`
- `GET` `/api/workspace/application/ListPossibleAccessRightMetricRemappings/{applicationId}/{armMetricId}`
- `GET` `/api/workspace/application/ListPossibleAccessRightMetrics/{applicationId}`
- `GET` `/api/workspace/application/ListPossibleMetricsOfAccessRights/{applicationId}`
- `GET` `/api/workspace/application/ListPossiblePermissionMetrics/{applicationId}`
- `GET` `/api/workspace/application/ModelMap/{applicationId}/{entityType}/{blockId}`
- `POST` `/api/workspace/application/Clone`
- `POST` `/api/workspace/application/Create/{organizationId}`
- `POST` `/api/workspace/application/ExportApplicationWSTypes/export-ws-types`
- `POST` `/api/workspace/application/FindSome/{organizationId}`
- `POST` `/api/workspace/application/FindSomePermissions/{organizationId}`
- `POST` `/api/workspace/application/FindSomePossibleAccessRightMetrics/{applicationId}`
- `POST` `/api/workspace/application/FindSomePossibleMetricsOfAccessRights/{applicationId}`
- `POST` `/api/workspace/application/FindSomePossiblePermissionMetrics/{applicationId}`
- `PUT` `/api/workspace/application/BatchSetApplicationsOwner/{organizationId}`
- `PUT` `/api/workspace/application/DisableApplicationLibrary/{applicationId}`
- `PUT` `/api/workspace/application/EnableApplicationLibrary/{applicationId}`
- `PUT` `/api/workspace/application/LockStructure/{applicationId}`
- `PUT` `/api/workspace/application/Rename/{applicationId}`
- `PUT` `/api/workspace/application/ResetSecurityObject/{applicationId}`
- `PUT` `/api/workspace/application/SetAllowResetAccessRightsForSharedBlocksDependencies/{applicationId}`
- `PUT` `/api/workspace/application/SetApplicationOwner/{applicationId}`
- `PUT` `/api/workspace/application/SetDisableAccessRightsInheritanceForBlocksInApp/{applicationId}`
- `PUT` `/api/workspace/application/SetLandingBoardsForApplication/{applicationId}`
- `PUT` `/api/workspace/application/SetStrictlyEnforceDefaultAccessRightInApp/{applicationId}`
- `PUT` `/api/workspace/application/UnlockStructure/{applicationId}`
- `PUT` `/api/workspace/application/UpdateColor/{applicationId}`
- `PUT` `/api/workspace/application/UpdateDescription/{applicationId}`
- `PUT` `/api/workspace/application/UpdatePermissionMetric/{applicationId}`
- `PUT` `/api/workspace/application/UpdateUserRoleMetricManagementMode/{applicationId}`

## ApplicationApi

- `GET` `/api/v1/applications`

## ApplicationInternal

- `DELETE` `/api/workspace/internals/application/BatchDelete/{organizationId}`
- `DELETE` `/api/workspace/internals/application/Delete/{applicationId}`
- `GET` `/api/workspace/internals/application/IdentifyMigrationCaseStrictlyEnforcedDefaultAccessRights/{applicationId}`
- `GET` `/api/workspace/internals/application/ListInternal`
- `POST` `/api/workspace/internals/application/EnableOrDisableTestAndDeploy/{applicationId}`
- `POST` `/api/workspace/internals/application/RepairSecurityObjects/{applicationId}`
- `PUT` `/api/workspace/internals/application/AddPermissionMetric/{applicationId}`
- `PUT` `/api/workspace/internals/application/SetApplicationOwnerInternal/{applicationId}`
- `PUT` `/api/workspace/internals/application/SetApplicationStatus/{organizationId}`
- `PUT` `/api/workspace/internals/application/UpdatePermissionMetric/{applicationId}`

## ApplicationUserRole

- `DELETE` `/api/workspace/applicationuserrole/DeleteRoleFromApplication/{applicationId}`
- `GET` `/api/workspace/applicationuserrole/FindAllRolesForApplication/{applicationId}`
- `GET` `/api/workspace/applicationuserrole/FindAllUserRoles/{organizationId}/{userId}`
- `GET` `/api/workspace/applicationuserrole/GetApplicationUserRoles/{applicationId}`
- `GET` `/api/workspace/applicationuserrole/GetCurrentUserRoleId/{applicationId}`
- `GET` `/api/workspace/applicationuserrole/ListRolesScenarioReadWriteAssignmentsLocalScenario/{applicationId}/{scenarioId}`
- `POST` `/api/workspace/applicationuserrole/ClaimAdminRole/{applicationId}`
- `POST` `/api/workspace/applicationuserrole/ClaimAdminRoleForMultipleApplications/{organizationId}`
- `POST` `/api/workspace/applicationuserrole/CreateRoleForApplication/{applicationId}`
- `POST` `/api/workspace/applicationuserrole/FindAllRolesForApplications/{organizationId}`
- `POST` `/api/workspace/applicationuserrole/ListRolesScenarioReadWriteAssignmentsSharedScenario/{organizationId}`
- `PUT` `/api/workspace/applicationuserrole/AssignApplicationRolesToUsers/{applicationId}`
- `PUT` `/api/workspace/applicationuserrole/BatchUpdateOrganizationRolesScenarioReadWriteAssignments/{organizationId}`
- `PUT` `/api/workspace/applicationuserrole/UpdateRoleForApplication/{applicationId}`
- `PUT` `/api/workspace/applicationuserrole/UpdateRolesScenarioReadWriteAssignmentsLocalScenario/{organizationId}`
- `PUT` `/api/workspace/applicationuserrole/UpdateRolesScenarioReadWriteAssignmentsSharedScenario/{organizationId}`

## ApplicationUserRoleInternal

- `GET` `/api/workspace/internals/applicationuserrole/FindAllRolesForApplication/{applicationId}`
- `GET` `/api/workspace/internals/applicationuserrole/FindAllUserRoles/{organizationId}/{userId}`

## BlocksApi

- `GET` `/api/v1/blocks`

## Board

- `DELETE` `/api/workspace/{applicationId}/board/Remove/{boardId}`
- `GET` `/api/workspace/{applicationId}/board/FindBoardIdsReferencingBlock`
- `GET` `/api/workspace/{applicationId}/board/FindBoardIdsReferencingViews`
- `GET` `/api/workspace/{applicationId}/board/Get/{boardId}`
- `GET` `/api/workspace/{applicationId}/board/GetAccess/{boardId}`
- `GET` `/api/workspace/{applicationId}/board/GetAllBoardsAllUsersPermissions`
- `GET` `/api/workspace/{applicationId}/board/GetAllUsersPermissions/{boardId}`
- `GET` `/api/workspace/{applicationId}/board/GetAllUsersPermissionsFromUserDimension/{boardId}`
- `GET` `/api/workspace/{applicationId}/board/GetPermission/{boardId}`
- `GET` `/api/workspace/{applicationId}/board/List`
- `GET` `/api/workspace/{applicationId}/board/ListPermissions`
- `POST` `/api/workspace/{applicationId}/board/Create`
- `POST` `/api/workspace/{applicationId}/board/Duplicate`
- `POST` `/api/workspace/{applicationId}/board/DuplicateWidget`
- `POST` `/api/workspace/{applicationId}/board/FindSome`
- `POST` `/api/workspace/{applicationId}/board/FindSomePermissions`
- `POST` `/api/workspace/{applicationId}/board/Update/{boardId}`
- `POST` `/api/workspace/{applicationId}/board/UpdateInheritApplicationPermissions/{boardId}`
- `POST` `/api/workspace/{applicationId}/board/UpdateUserActionsCanCustomizeViews/{boardId}`
- `POST` `/api/workspace/{applicationId}/board/UpdateUserActionsCanExploreBlocks/{boardId}`
- `PUT` `/api/workspace/{applicationId}/board/ClearPermissionMetrics/{boardId}`
- `PUT` `/api/workspace/{applicationId}/board/MoveIntoFolder/{boardId}`
- `PUT` `/api/workspace/{applicationId}/board/SetPermissionMetrics/{boardId}`
- `PUT` `/api/workspace/{applicationId}/board/UpdateBlocks/{boardId}`
- `PUT` `/api/workspace/{applicationId}/board/UpdateBoardInfo/{boardId}`
- `PUT` `/api/workspace/{applicationId}/board/UpdatePageConfigurations/{boardId}`

## Calendar

- `DELETE` `/api/workspace/{applicationId}/calendar/Remove/{calendarId}`
- `GET` `/api/workspace/{applicationId}/calendar/Get/{calendarId}`
- `GET` `/api/workspace/{applicationId}/calendar/GetTimeDimensionConstraints/{calendarType}`
- `GET` `/api/workspace/{applicationId}/calendar/List`
- `POST` `/api/workspace/{applicationId}/calendar/Create`
- `POST` `/api/workspace/{applicationId}/calendar/RemoveTimeDimension/{calendarId}`
- `PUT` `/api/workspace/{applicationId}/calendar/AddTimeDimension/{calendarId}`
- `PUT` `/api/workspace/{applicationId}/calendar/ChangeFiscalYear/{calendarId}`
- `PUT` `/api/workspace/{applicationId}/calendar/EnableActualVsForecat/{calendarId}`
- `PUT` `/api/workspace/{applicationId}/calendar/ExpandCalendar/{calendarId}`

## CalendarInternal

- `POST` `/api/workspace/internals/list/UpdateFiscalYear`

## Clone

- `DELETE` `/api/workspace/clone/{organizationId}/BatchDeleteSnapshotCloneGroup`
- `DELETE` `/api/workspace/clone/{organizationId}/RemoveApplicationFromSnapshotGroup`
- `GET` `/api/workspace/clone/{organizationId}/AllSnapshotCloneGroups`
- `GET` `/api/workspace/clone/{organizationId}/ListActiveCloneJobsForOrganization`
- `GET` `/api/workspace/clone/{organizationId}/NumberOfRemainingSnapshots`
- `POST` `/api/workspace/clone/{organizationId}/ClonePreview`
- `POST` `/api/workspace/clone/{organizationId}/FindSomeCloneJobs`
- `POST` `/api/workspace/clone/{organizationId}/FindSomeSnapshotCloneGroups`
- `PUT` `/api/workspace/clone/{organizationId}/AbortAndDeleteApplicationV2`
- `PUT` `/api/workspace/clone/{organizationId}/RenameSnapshotCloneGroup`
- `PUT` `/api/workspace/clone/{organizationId}/ToggleIsComparable`

## CloneData

- `PUT` `/api/workspace/cloneData/{organizationId}/CloneData/{applicationId}`
- `PUT` `/api/workspace/cloneData/{organizationId}/CloneDataFromConfiguration/{applicationId}/CloneDataFromConfiguration`

## CloneDataConfiguration

- `DELETE` `/api/workspace/cloneDataConfiguration/{organizationId}/DeleteConfiguration/{applicationId}/{configurationId}`
- `GET` `/api/workspace/cloneDataConfiguration/{organizationId}/FindConfiguration/{applicationId}/{configurationId}`
- `GET` `/api/workspace/cloneDataConfiguration/{organizationId}/ListConfigurations/{applicationId}`
- `POST` `/api/workspace/cloneDataConfiguration/{organizationId}/CreateConfiguration/{applicationId}`
- `POST` `/api/workspace/cloneDataConfiguration/{organizationId}/DuplicateConfiguration/{applicationId}/Duplicate`
- `POST` `/api/workspace/cloneDataConfiguration/{organizationId}/FindSomeConfigurations/{applicationId}/FindSome`
- `PUT` `/api/workspace/cloneDataConfiguration/{organizationId}/UpdateConfiguration/{applicationId}`

## CloneDataConfigurationInternal

- `GET` `/api/workspace/internals/cloneDataConfiguration/ListForOrganization/{organizationId}`

## CloneInternal

- `DELETE` `/api/workspace/internals/clone/TriggerCloneGroupsDeletion/{organizationId}/{cloneGroupType}`
- `GET` `/api/workspace/internals/clone/AllSnapshotCloneGroups/{organizationId}/{applicationId}`
- `GET` `/api/workspace/internals/clone/AllSnapshotCloneGroupsForOrganization/{organizationId}`
- `GET` `/api/workspace/internals/clone/GetSnapshotUsage/{organizationId}`
- `GET` `/api/workspace/internals/clone/HasOngoingCloneJob/{organizationId}`
- `GET` `/api/workspace/internals/clone/ListForOrganization/{organizationId}`
- `PUT` `/api/workspace/internals/clone/AbortV2/{organizationId}/{cloneJobId}`

## Conversation

- `DELETE` `/api/workspace/{applicationId}/conversation/DeleteMessage/{conversationId}`
- `GET` `/api/workspace/{applicationId}/conversation/Get/{conversationId}`
- `GET` `/api/workspace/{applicationId}/conversation/List`
- `POST` `/api/workspace/{applicationId}/conversation/AddMessage/{conversationId}`
- `POST` `/api/workspace/{applicationId}/conversation/Create`
- `POST` `/api/workspace/{applicationId}/conversation/Subscribe/{conversationId}`
- `PUT` `/api/workspace/{applicationId}/conversation/SwitchConversationToPrivate/{conversationId}`
- `PUT` `/api/workspace/{applicationId}/conversation/SwitchConversationToPublic/{conversationId}`
- `PUT` `/api/workspace/{applicationId}/conversation/Unsubscribe/{conversationId}`
- `PUT` `/api/workspace/{applicationId}/conversation/UnsubscribeUser/{conversationId}`
- `PUT` `/api/workspace/{applicationId}/conversation/UpdateAuthorizedUsers/{conversationId}`
- `PUT` `/api/workspace/{applicationId}/conversation/UpdateMessage/{conversationId}`
- `PUT` `/api/workspace/{applicationId}/conversation/UpdateStatus/{conversationId}`

## Cycle

- `DELETE` `/api/workspace/{applicationId}/cycle/DeleteCycle`
- `GET` `/api/workspace/{applicationId}/cycle/GetApplicationCycles`
- `POST` `/api/workspace/{applicationId}/cycle/CreateCycle`
- `POST` `/api/workspace/{applicationId}/cycle/GetSomeCycles`
- `PUT` `/api/workspace/{applicationId}/cycle/UpdateCycle`

## CycleEntity

- `DELETE` `/api/workspace/{applicationId}/cycleEntity/DeleteCycleEntity/{cycleId}`
- `GET` `/api/workspace/{applicationId}/cycleEntity/FindCycleEntity/{cycleId}`
- `GET` `/api/workspace/{applicationId}/cycleEntity/GetApplicationCycleEntities`
- `GET` `/api/workspace/{applicationId}/cycleEntity/GetApplicationCyclesCircularDependencyInfo`
- `POST` `/api/workspace/{applicationId}/cycleEntity/CreateCycleEntity`
- `POST` `/api/workspace/{applicationId}/cycleEntity/GetSomeApplicationCycleEntities`
- `POST` `/api/workspace/{applicationId}/cycleEntity/GetSomeCyclesCircularDependencyInfo`
- `PUT` `/api/workspace/{applicationId}/cycleEntity/UpdateCycleEntity/{cycleId}`

## CycleEntityInternal

- `POST` `/api/workspace/internals/{applicationId}/cycleEntity/ForkCycle/{cycleId}/fork/{scenarioId}`

## CycleInternal

- `GET` `/api/workspace/internals/{applicationId}/cycle/GetCycleInformation`

## DataModelInternal

- `GET` `/api/workspace/internals/datamodel/Introspect/{needle}`
- `POST` `/api/workspace/internals/datamodel/QueryDependencies`

## DatabaseMigrationInternal

- `GET` `/api/workspace/internals/databasemigration/ListOngoingMigrations`
- `GET` `/api/workspace/internals/databasemigration/ListOngoingMigrationsWithApiKey`
- `GET` `/api/workspace/internals/databasemigration/ShowOngoingMigration`
- `GET` `/api/workspace/internals/databasemigration/ShowOngoingMigrationWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/AbortMigration`
- `POST` `/api/workspace/internals/databasemigration/AbortMigrationWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/CancelActiveSynchronization`
- `POST` `/api/workspace/internals/databasemigration/CancelActiveSynchronizationWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/CleanupOrphans`
- `POST` `/api/workspace/internals/databasemigration/CleanupOrphansWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/CreateMigration`
- `POST` `/api/workspace/internals/databasemigration/CreateMigrationWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/FinalizeMigration`
- `POST` `/api/workspace/internals/databasemigration/FinalizeMigrationWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/ResumeStuckActiveSynchronization`
- `POST` `/api/workspace/internals/databasemigration/ResumeStuckActiveSynchronizationWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/RollbackMigration`
- `POST` `/api/workspace/internals/databasemigration/RollbackMigrationWithApiKey`
- `POST` `/api/workspace/internals/databasemigration/StartNewSynchronization`
- `POST` `/api/workspace/internals/databasemigration/StartNewSynchronizationWithApiKey`
- `PUT` `/api/workspace/internals/databasemigration/SetParallelism`
- `PUT` `/api/workspace/internals/databasemigration/SetParallelismWithApiKey`

## DatasetInternal

- `GET` `/api/workspace/internals/dataset/Get/{organizationId}/{datasetId}`
- `GET` `/api/workspace/internals/dataset/GetRawDatasetData/{organizationId}/{datasetId}`
- `GET` `/api/workspace/internals/dataset/GetRowCount/{organizationId}/{datasetId}`
- `GET` `/api/workspace/internals/dataset/ListDatasetsInApplication/{organizationId}`
- `POST` `/api/workspace/internals/dataset/QueryDatasetExistence/{organizationId}`
- `POST` `/api/workspace/internals/dataset/Remove/{organizationId}/{datasetId}`

## DatasetMonitoringInternal

- `GET` `/api/workspace/internals/dataset/GetLargestDatasetsByRowCount`
- `GET` `/api/workspace/internals/dataset/GetMostFrequentValue`
- `GET` `/api/workspace/internals/dataset/GetTopDatasetColumnsByMostFrequentValue`
- `POST` `/api/workspace/internals/dataset/GeGetAllDatasetEntities`

## DatasetStorageFederationInternal

- `POST` `/api/workspace/internals/datasetstoragefederation/CreateDatasetDatabase/{organizationId}`

## DebugInternal

- `GET` `/api/workspace/internals/debug/Delay`
- `GET` `/api/workspace/internals/debug/Log`
- `GET` `/api/workspace/internals/debug/LogCurrentTestEnd`
- `GET` `/api/workspace/internals/debug/LogCurrentTestStart`
- `POST` `/api/workspace/internals/debug/TriggerTestJob`

## Export

- `GET` `/api/export/view/{viewId}`
- `POST` `/api/export/list/{listId}`
- `POST` `/api/export/metric/{metricId}`
- `POST` `/api/export/table/{tableId}`

## ExportV1

- `GET` `/api/v1/export/view/{viewId}`
- `POST` `/api/v1/export/list/{listId}`
- `POST` `/api/v1/export/metric/{metricId}`
- `POST` `/api/v1/export/table/{tableId}`

## FeatureFlag

- `GET` `/api/workspace/featureflag/Flags/{organizationId}`

## FeatureFlagInternal

- `DELETE` `/api/workspace/internals/featureflag/DeleteFlag/{flag}`
- `GET` `/api/workspace/internals/featureflag/FlagOverrides/{flag}`
- `GET` `/api/workspace/internals/featureflag/FlagValues/{organizationId}`
- `GET` `/api/workspace/internals/featureflag/GetDefaultStates`
- `GET` `/api/workspace/internals/featureflag/OrganizationFlags/{organizationId}`
- `PUT` `/api/workspace/internals/featureflag/BatchDisableFlag/{flag}`
- `PUT` `/api/workspace/internals/featureflag/BatchEnableFlag/{flag}`
- `PUT` `/api/workspace/internals/featureflag/DisableFlag/{flag}`
- `PUT` `/api/workspace/internals/featureflag/EnableFlag/{flag}`

## Folder

- `DELETE` `/api/workspace/{applicationId}/folder/Remove/{folderId}`
- `GET` `/api/workspace/{applicationId}/folder/List`
- `POST` `/api/workspace/{applicationId}/folder/Create`
- `POST` `/api/workspace/{applicationId}/folder/CreateFolder`
- `POST` `/api/workspace/{applicationId}/folder/FindSome`
- `PUT` `/api/workspace/{applicationId}/folder/Rename/{folderId}`
- `PUT` `/api/workspace/{applicationId}/folder/RenameFolder/{folderId}`

## Formula

- `DELETE` `/api/workspace/{applicationId}/formula/RemoveOnMetricViaFormulaGroup`
- `GET` `/api/workspace/{applicationId}/formula/CanFormulaBeCopiedAsValues`
- `GET` `/api/workspace/{applicationId}/formula/FormulaExists/{formulaId}`
- `GET` `/api/workspace/{applicationId}/formula/Get/{formulaId}`
- `POST` `/api/workspace/{applicationId}/formula/AutoFormatFormula`
- `POST` `/api/workspace/{applicationId}/formula/BatchFormatForAuditTrail`
- `POST` `/api/workspace/{applicationId}/formula/CompileFormula`
- `POST` `/api/workspace/{applicationId}/formula/CompileFormulaForTarget`
- `POST` `/api/workspace/{applicationId}/formula/CopyAsValues`
- `POST` `/api/workspace/{applicationId}/formula/CreateOnList`
- `POST` `/api/workspace/{applicationId}/formula/CreateOnMetric/{metricId}/{formulaGroupId}`
- `POST` `/api/workspace/{applicationId}/formula/DrillToSources/{formulaId}`
- `POST` `/api/workspace/{applicationId}/formula/GetFormulae`
- `POST` `/api/workspace/{applicationId}/formula/GetFormulaeShared`
- `POST` `/api/workspace/{applicationId}/formula/ValidateListPropertyFormula`
- `POST` `/api/workspace/{applicationId}/formula/ValidateMetricFormula`

## FormulaAutocomplete

- `GET` `/api/workspace/{applicationId}/autocomplete/FindListItems/{dimensionListId}`
- `GET` `/api/workspace/{applicationId}/autocomplete/GetCompletionDetails`

## FormulaDiffInternal

- `DELETE` `/api/workspace/internals/formuladiff/CleanUpDefaultFormulaOption`
- `DELETE` `/api/workspace/internals/formuladiff/RemoveDefaultFormulaOption`
- `GET` `/api/workspace/internals/formuladiff/DownloadDiffReport`
- `GET` `/api/workspace/internals/formuladiff/GetDetailedOrganizationRunResult`
- `GET` `/api/workspace/internals/formuladiff/ListDefaultFormulaOption`
- `GET` `/api/workspace/internals/formuladiff/ListRuns`
- `GET` `/api/workspace/internals/formuladiff/ListSomeRuns`
- `GET` `/api/workspace/internals/formuladiff/RunResultPerOrganization`
- `POST` `/api/workspace/internals/formuladiff/AddDefaultFormulaOption`
- `POST` `/api/workspace/internals/formuladiff/ComputeDiffForTask`
- `POST` `/api/workspace/internals/formuladiff/CreateRun`
- `POST` `/api/workspace/internals/formuladiff/DeleteOrgTasks`
- `POST` `/api/workspace/internals/formuladiff/DeleteRun`
- `POST` `/api/workspace/internals/formuladiff/ForceRelease`
- `POST` `/api/workspace/internals/formuladiff/ListFormulasFromConfiguration`
- `POST` `/api/workspace/internals/formuladiff/RecomputeDiffOnOrganization`
- `POST` `/api/workspace/internals/formuladiff/RecomputeDiffTasks`
- `POST` `/api/workspace/internals/formuladiff/UpdateRunStatus`

## FormulaInternal

- `GET` `/api/workspace/internals/formula/FilterFormulasMatchingXPath`
- `GET` `/api/workspace/internals/formula/FindAllFormulasInApplication/{organizationId}/{applicationId}`
- `GET` `/api/workspace/internals/formula/FindFormulasByInvalidity`
- `GET` `/api/workspace/internals/formula/FindFormulasByOrganization`
- `GET` `/api/workspace/internals/formula/FindFormulasBySearchId`
- `GET` `/api/workspace/internals/formula/FindFormulasByText`
- `GET` `/api/workspace/internals/formula/FormatAsDebug/{organizationId}/{applicationId}/{formulaId}`
- `GET` `/api/workspace/internals/formula/FormatAsJson/{organizationId}/{applicationId}/{formulaId}`
- `GET` `/api/workspace/internals/formula/FormatAsPretty/{organizationId}/{applicationId}/{formulaId}`
- `GET` `/api/workspace/internals/formula/GetFormulaSourceLinks`
- `POST` `/api/workspace/internals/formula/CompileFormulaAccessRightsInternal`
- `POST` `/api/workspace/internals/formula/CompileFormulaInternal`
- `POST` `/api/workspace/internals/formula/CompileManyFormulaInternal`
- `POST` `/api/workspace/internals/formula/Compute/{organizationId}/{applicationId}`
- `POST` `/api/workspace/internals/formula/ExportManyFormulas`
- `POST` `/api/workspace/internals/formula/GetFormulaSourceLinksForTarget/{applicationId}`
- `POST` `/api/workspace/internals/formula/GetFormulae`
- `POST` `/api/workspace/internals/formula/InvalidByExecutionErrorCode`
- `POST` `/api/workspace/internals/formula/ListFormulaHistoryForTarget/{applicationId}`
- `POST` `/api/workspace/internals/formula/Preview/{applicationId}`
- `POST` `/api/workspace/internals/formula/ProfileForTarget/{applicationId}`
- `POST` `/api/workspace/internals/formula/Repair/{organizationId}/{applicationId}/{formulaId}`
- `POST` `/api/workspace/internals/formula/ResyncFormulaWithParentGroup`
- `PUT` `/api/workspace/internals/formula/CompileAsDebug/{organizationId}/{applicationId}`
- `PUT` `/api/workspace/internals/formula/CompileAsJson/{organizationId}/{applicationId}`

## GSheet

- `GET` `/api/workspace/gsheet/v1/AvailableOrganizations`
- `GET` `/api/workspace/gsheet/v1/CurrentUser/{organizationId}`
- `GET` `/api/workspace/gsheet/v1/Organization/{organizationId}`
- `GET` `/api/workspace/gsheet/v1/OrganizationMetadata/{organizationId}`
- `GET` `/api/workspace/gsheet/v1/ViewPagination/{applicationId}/{viewId}`
- `POST` `/api/workspace/gsheet/v1/PullData/{applicationId}/{viewId}`

## IntrospectorGadgetInternal

- `GET` `/api/workspace/internals/model-introspector/Gogo/{needle}`

## Issue

- `GET` `/api/workspace/{applicationId}/issue/FindFromApplication`
- `POST` `/api/workspace/{applicationId}/issue/FindFromApplicationByFormulaId`

## JobDebugInternal

- `POST` `/api/workspace/internals/jobdebug/DeserializePayload`

## JobProfiling

- `GET` `/api/workspace/{organizationId}/job-profiling/GetChangeProfile/{changeId}`

## JobProfilingInternal

- `POST` `/api/workspace/internals/{organizationId}/job-profiling/GetSlowestChanges`

## List

- `DELETE` `/api/workspace/{applicationId}/list/DeleteSelectedListModalities`
- `DELETE` `/api/workspace/{applicationId}/list/Remove/{listId}`
- `GET` `/api/workspace/list/{organizationId}/ListForOrganization`
- `GET` `/api/workspace/{applicationId}/list/CanDuplicateList/{listId}`
- `GET` `/api/workspace/{applicationId}/list/Get/{listId}`
- `GET` `/api/workspace/{applicationId}/list/GetAccessRightsInfo/{listId}`
- `GET` `/api/workspace/{applicationId}/list/GetBlockSharingPlanForMoveToApplication/{listId}`
- `GET` `/api/workspace/{applicationId}/list/GetBlockSharingPlanForSharingList/{listId}`
- `GET` `/api/workspace/{applicationId}/list/GetBlockSharingPlanForSubstitution`
- `GET` `/api/workspace/{applicationId}/list/GetDisplayData/{listId}`
- `GET` `/api/workspace/{applicationId}/list/GetUsages/{listId}`
- `GET` `/api/workspace/{applicationId}/list/GetUsagesAsMetricDimension/{dimensionId}`
- `GET` `/api/workspace/{applicationId}/list/ListForApplication`
- `GET` `/api/workspace/{applicationId}/list/ListPermissions`
- `GET` `/api/workspace/{organizationId}/list/ListAllSharedListsAcrossOrganization`
- `POST` `/api/workspace/list/{organizationId}/FindModalityLabels`
- `POST` `/api/workspace/list/{organizationId}/FindSomeForOrganization`
- `POST` `/api/workspace/{applicationId}/list/AddRow`
- `POST` `/api/workspace/{applicationId}/list/AddRows`
- `POST` `/api/workspace/{applicationId}/list/CreateWithDefaultView`
- `POST` `/api/workspace/{applicationId}/list/DuplicateList`
- `POST` `/api/workspace/{applicationId}/list/ExportAdditionalTypes/export-ws-types`
- `POST` `/api/workspace/{applicationId}/list/FindDisplayData/{listId}`
- `POST` `/api/workspace/{applicationId}/list/FindListInputDropdownItems`
- `POST` `/api/workspace/{applicationId}/list/FindSomeForApplication`
- `POST` `/api/workspace/{applicationId}/list/FindSomeListPermissions`
- `POST` `/api/workspace/{applicationId}/list/GetBlockSharingPlanForAddingProperties/{listId}`
- `POST` `/api/workspace/{applicationId}/list/GetBlockSharingPlanForUpdatingProperty/{listId}`
- `POST` `/api/workspace/{applicationId}/list/RenameSome`
- `POST` `/api/workspace/{applicationId}/list/Substitute`
- `PUT` `/api/workspace/{applicationId}/list/BulkUnshare`
- `PUT` `/api/workspace/{applicationId}/list/ChangeAiMetadata/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/ChangeDescription/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/EnableModalityDisplayColorOverride`
- `PUT` `/api/workspace/{applicationId}/list/MoveIntoFolder/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/MoveRowAbsolute`
- `PUT` `/api/workspace/{applicationId}/list/MoveRowRelative`
- `PUT` `/api/workspace/{applicationId}/list/MoveToApplication/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/ReOrder`
- `PUT` `/api/workspace/{applicationId}/list/Rename/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/SetDefaultView/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/SetDisplayNames/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/SetInputDropdownConfig/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/SetInputtedValue`
- `PUT` `/api/workspace/{applicationId}/list/SetInputtedValues`
- `PUT` `/api/workspace/{applicationId}/list/SetInputtedValuesWithNewRows`
- `PUT` `/api/workspace/{applicationId}/list/ToggleAllowEditItemsWhenLocked/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/ToggleDefaultToSingleModality/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/ToggleIsDimension/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/ToggleManualSave/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/ToggleReadableByEveryone/{listId}`
- `PUT` `/api/workspace/{applicationId}/list/UpdateSharingStatus/{listId}`

## ListInternal

- `GET` `/api/workspace/internals/list/GetAll`
- `GET` `/api/workspace/internals/list/ListForApplication`
- `POST` `/api/workspace/internals/list/AnonymizeListData`
- `POST` `/api/workspace/internals/list/DeleteSublist`
- `POST` `/api/workspace/internals/list/MigrateListOriginTrackers`
- `POST` `/api/workspace/internals/list/RegenerateSublistsJobs`
- `POST` `/api/workspace/internals/list/RetriggerSublistsJobs`
- `POST` `/api/workspace/internals/list/TruncateSublistsDatasets`

## ListProperty

- `DELETE` `/api/workspace/{applicationId}/list/{listId}/property/Remove`
- `DELETE` `/api/workspace/{applicationId}/list/{listId}/property/RemoveAutogeneratedProperties`
- `GET` `/api/workspace/{applicationId}/list/{listId}/property/GetUsages`
- `POST` `/api/workspace/{applicationId}/list/{listId}/property/Add`
- `POST` `/api/workspace/{applicationId}/list/{listId}/property/AddAutogeneratedProperties`
- `POST` `/api/workspace/{applicationId}/list/{listId}/property/AddMultiple`
- `PUT` `/api/workspace/{applicationId}/list/{listId}/property/ChangeAiMetadata`
- `PUT` `/api/workspace/{applicationId}/list/{listId}/property/Update`
- `PUT` `/api/workspace/{applicationId}/list/{listId}/property/UpdateDefaultProperty`
- `PUT` `/api/workspace/{applicationId}/list/{listId}/property/UpdateDisplayProperty`

## Metric

- `DELETE` `/api/workspace/{applicationId}/metric/Remove/{metricId}`
- `GET` `/api/workspace/metric/{organizationId}/ListForOrganization`
- `GET` `/api/workspace/{applicationId}/metric/CanFormulaBeCopiedAsValues/{metricId}`
- `GET` `/api/workspace/{applicationId}/metric/CanSafelyDisableOverride/{metricId}`
- `GET` `/api/workspace/{applicationId}/metric/Get/{metricId}`
- `GET` `/api/workspace/{applicationId}/metric/GetAccessRightsInfo/{metricId}`
- `GET` `/api/workspace/{applicationId}/metric/GetFormulaGroups/{metricId}`
- `GET` `/api/workspace/{applicationId}/metric/GetUsages/{metricId}`
- `GET` `/api/workspace/{applicationId}/metric/GetValidMetricsForCopyScenarioInputs`
- `GET` `/api/workspace/{applicationId}/metric/HasUserInputsInFormulaGroupV2/{metricId}`
- `GET` `/api/workspace/{applicationId}/metric/ListForApplication`
- `GET` `/api/workspace/{organizationId}/metric/ListAllSharedAcrossOrganization`
- `POST` `/api/workspace/metric/{organizationId}/FindSomeForOrganization`
- `POST` `/api/workspace/{applicationId}/metric/CreateAutomatic`
- `POST` `/api/workspace/{applicationId}/metric/CreateFromAccessRights`
- `POST` `/api/workspace/{applicationId}/metric/CreateFromConfiguration`
- `POST` `/api/workspace/{applicationId}/metric/CreateFromCopy`
- `POST` `/api/workspace/{applicationId}/metric/CreateFromDrillDown`
- `POST` `/api/workspace/{applicationId}/metric/CreateFromLayout`
- `POST` `/api/workspace/{applicationId}/metric/DrillDown/{metricId}`
- `POST` `/api/workspace/{applicationId}/metric/DuplicateMetric`
- `POST` `/api/workspace/{applicationId}/metric/DuplicateMetrics`
- `POST` `/api/workspace/{applicationId}/metric/ExportAdditionalTypes/export-ws-types`
- `POST` `/api/workspace/{applicationId}/metric/FindSomeForApplication`
- `POST` `/api/workspace/{applicationId}/metric/GetBlockSharingPlanForDimensionsUpdate`
- `POST` `/api/workspace/{applicationId}/metric/GetBlockSharingPlanForSharingMetrics`
- `POST` `/api/workspace/{applicationId}/metric/GetBlockSharingPlanForTypeChange`
- `POST` `/api/workspace/{applicationId}/metric/GetSomeMetricStructures`
- `POST` `/api/workspace/{applicationId}/metric/RenameSome`
- `POST` `/api/workspace/{applicationId}/metric/SetDefaultAggregators/{metricId}`
- `POST` `/api/workspace/{applicationId}/metric/UpdateFormulaGroupsScope/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/BatchChangeType`
- `PUT` `/api/workspace/{applicationId}/metric/BatchInput/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/BatchMoveIntoFolder`
- `PUT` `/api/workspace/{applicationId}/metric/BatchRemove`
- `PUT` `/api/workspace/{applicationId}/metric/BatchUpdateDimensions`
- `PUT` `/api/workspace/{applicationId}/metric/BatchUpdateVisibility`
- `PUT` `/api/workspace/{applicationId}/metric/ChangeAiMetadata/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/ChangeAiVisibility/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/ChangeDescription/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/ChangeType/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/CopyFormulaGroupAsUserInputs/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/CopyScenarioInputs`
- `PUT` `/api/workspace/{applicationId}/metric/DeleteInputs`
- `PUT` `/api/workspace/{applicationId}/metric/MoveIntoFolder/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/PromoteAccessRightsMetric`
- `PUT` `/api/workspace/{applicationId}/metric/PromoteMetric`
- `PUT` `/api/workspace/{applicationId}/metric/Rename/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/ResetFormulaGroupsAndUserInputs/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/SetDefaultFormatDefinition/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/SetDefaultView/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/SetDisplayNames/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/ToggleInputOnAllScenarios/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/ToggleManualSave/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/ToggleReadableByEveryone/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/UpdateDimensions/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/UpdateDisplayColor/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/UpdateMetricVisibility/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/UpdateMultipleOverrides/{metricId}`
- `PUT` `/api/workspace/{applicationId}/metric/UpdateOverride/{metricId}`
- `PUT` `/api/workspace/{organizationId}/metric/BatchInputMultipleMetrics`

## MetricInternal

- `GET` `/api/workspace/internals/metric/GetAll`
- `GET` `/api/workspace/internals/metric/GetFormulaGroups`
- `GET` `/api/workspace/internals/metric/GetFromOrganization`
- `GET` `/api/workspace/internals/metric/GetInputOverrideInfo`
- `GET` `/api/workspace/internals/metric/GetMetricsBlockingResync/{metricId}`
- `GET` `/api/workspace/internals/metric/ListForApplication`
- `POST` `/api/workspace/internals/metric/CorruptMetricByForceResync`
- `POST` `/api/workspace/internals/metric/GetSomeMetricStructures`
- `POST` `/api/workspace/internals/metric/ResyncFormulaGroups`
- `POST` `/api/workspace/internals/metric/ResyncMetrics`
- `PUT` `/api/workspace/internals/metric/UpdateMetricVisibilityIgnoreMetricDependencies`

## ModelPerformance

- `GET` `/api/workspace/{applicationId}/model-performance/GetInsightProfileForMetric/{scenarioId}/{metricId}`
- `GET` `/api/workspace/{applicationId}/model-performance/GetInsightProfileForTable/{scenarioId}/{tableId}`
- `GET` `/api/workspace/{applicationId}/model-performance/GetInsightsForApplication`

## OperationMonitoringInternal

- `GET` `/api/workspace/internals/operation/GetAllContinuationsInError`
- `GET` `/api/workspace/internals/operation/GetOperationContinuation`
- `GET` `/api/workspace/internals/operation/GetOperationContinuationsWithoutPayload`
- `GET` `/api/workspace/internals/operation/GetOperations`
- `POST` `/api/workspace/internals/operation/DeleteOperations`
- `POST` `/api/workspace/internals/operation/RetryContinuations`

## Organization

- `GET` `/api/workspace/organization/{organizationId}`
- `GET` `/api/workspace/organization/{organizationId}/GetCurrentPermission`
- `GET` `/api/workspace/organization/{organizationId}/GetRoles`
- `GET` `/api/workspace/organization/{organizationId}/GetRolesDatasetIds`
- `GET` `/api/workspace/organization/{organizationId}/GetUserDatasetId`
- `GET` `/api/workspace/organization/{organizationId}/GetUsers`
- `POST` `/api/workspace/organization/{organizationId}/ExportOrganizationDatasetEventTypes/export-ws-types`
- `POST` `/api/workspace/organization/{organizationId}/FindSomeRoles`
- `POST` `/api/workspace/organization/{organizationId}/FindSomeUsers`
- `PUT` `/api/workspace/organization/{organizationId}/SetAllowResetAccessRightsForSharedBlocksDependencies`
- `PUT` `/api/workspace/organization/{organizationId}/SetDisableAccessRightsInheritanceForBlocksInApp`
- `PUT` `/api/workspace/organization/{organizationId}/UpdateDisplaySetting`
- `PUT` `/api/workspace/organization/{organizationId}/UpdateImageAllowListDomains`
- `PUT` `/api/workspace/organization/{organizationId}/UpdateUserRole/{userId}`

## OrganizationCalendars

- `GET` `/api/workspace/calendars/ListSharedCalendars`

## OrganizationInternal

- `DELETE` `/api/workspace/internals/organization/DeleteUsersFromUserDimension`
- `GET` `/api/workspace/internals/organization/Get`
- `GET` `/api/workspace/internals/organization/GetUnusedBlocks`
- `GET` `/api/workspace/internals/organization/JobActivations`
- `GET` `/api/workspace/internals/organization/List`
- `GET` `/api/workspace/internals/organization/Users`
- `GET` `/api/workspace/internals/organization/UsersWithOrganizationPermissions`
- `POST` `/api/workspace/internals/organization/InsertUsersUserDimension`
- `PUT` `/api/workspace/internals/organization/OverrideJobActivation`
- `PUT` `/api/workspace/internals/organization/ResetJobActivation`
- `PUT` `/api/workspace/internals/organization/ResetRolesDefinitionForAdminApp`

## PatchInternal

- `GET` `/api/workspace/internals/patch/List`
- `GET` `/api/workspace/internals/patch/ListByOrganization/{organizationId}`
- `GET` `/api/workspace/internals/patch/ListByPatch/{patchName}`
- `POST` `/api/workspace/internals/patch/ApplyPatch/{patchName}`
- `POST` `/api/workspace/internals/patch/ApplyPatchOnOrganizations/{patchName}`
- `POST` `/api/workspace/internals/patch/ResetPatch/{patchName}`
- `POST` `/api/workspace/internals/patch/ResetPatchOnOrganizations/{patchName}`
- `POST` `/api/workspace/internals/patch/RevertPatch/{patchName}`
- `POST` `/api/workspace/internals/patch/RevertPatchOnOrganizations/{patchName}`

## Permission

- `GET` `/api/workspace/permission/List/{applicationId}`
- `POST` `/api/workspace/permission/FindSome/{applicationId}`

## RemapAndCopyInternal

- `GET` `/api/workspace/internals/remap-and-copy/FindScenarioMappings/{organizationId}`
- `POST` `/api/workspace/internals/remap-and-copy/ExecuteRemapAndCopy/{organizationId}`
- `POST` `/api/workspace/internals/remap-and-copy/FindTransferCandidate/{organizationId}`
- `PUT` `/api/workspace/internals/remap-and-copy/GetDimensionsCompatibilities/{organizationId}`

## Scenario

- `GET` `/api/workspace/{applicationId}/scenario/Find/{scenarioId}`
- `GET` `/api/workspace/{applicationId}/scenario/FindDefault`
- `GET` `/api/workspace/{applicationId}/scenario/GetSettings`
- `GET` `/api/workspace/{applicationId}/scenario/List`
- `GET` `/api/workspace/{applicationId}/scenario/ListScenarioPermissions`
- `POST` `/api/workspace/scenario/FindSomeScenarioPermissions/{organizationId}`
- `POST` `/api/workspace/scenario/ListInOrganization/{organizationId}`
- `POST` `/api/workspace/{applicationId}/scenario/ChangeDescription/{scenarioId}`
- `POST` `/api/workspace/{applicationId}/scenario/ChangeInputsRestrictions/{scenarioId}`
- `POST` `/api/workspace/{applicationId}/scenario/Create`
- `POST` `/api/workspace/{applicationId}/scenario/CreateWithScenarioGroup`
- `POST` `/api/workspace/{applicationId}/scenario/Delete/{scenarioId}`
- `POST` `/api/workspace/{applicationId}/scenario/DeleteWithScenarioGroup/{scenarioId}`
- `POST` `/api/workspace/{applicationId}/scenario/FindSome`
- `POST` `/api/workspace/{applicationId}/scenario/Rename/{scenarioId}`
- `PUT` `/api/workspace/{applicationId}/scenario/DisableScenario`
- `PUT` `/api/workspace/{applicationId}/scenario/EnableScenario`
- `PUT` `/api/workspace/{applicationId}/scenario/UpdateDisplayColor/{scenarioId}`

## ScenarioGroup

- `GET` `/api/workspace/scenariogroup/FindDefault/{organizationId}`
- `GET` `/api/workspace/scenariogroup/List/{organizationId}`
- `GET` `/api/workspace/scenariogroup/ListWithDeleted/{organizationId}`

## ScenarioInternal

- `GET` `/api/workspace/internals/scenario/FindDefault`
- `GET` `/api/workspace/internals/scenario/FindMetricThatShouldNotBeForked`
- `GET` `/api/workspace/internals/scenario/GetScenarioMap`
- `GET` `/api/workspace/internals/scenario/InspectFork`
- `GET` `/api/workspace/internals/scenario/List`
- `GET` `/api/workspace/internals/scenario/ListInOrganization`
- `POST` `/api/workspace/internals/scenario/FixMissingForkInApplication`
- `POST` `/api/workspace/internals/scenario/FixMissingForkInOrganization`
- `POST` `/api/workspace/internals/scenario/ForkMetricInScenario`
- `POST` `/api/workspace/internals/scenario/ForkMetricsInScenarios`

## Sequence

- `DELETE` `/api/workspace/{applicationId}/sequence/Delete/{sequenceId}`
- `GET` `/api/workspace/{applicationId}/sequence/Get/{sequenceId}`
- `GET` `/api/workspace/{applicationId}/sequence/List`
- `POST` `/api/workspace/{applicationId}/sequence/Create`
- `POST` `/api/workspace/{applicationId}/sequence/Duplicate`
- `POST` `/api/workspace/{applicationId}/sequence/FindSome`
- `POST` `/api/workspace/{applicationId}/sequence/Update/{sequenceId}`

## SimulationInternal

- `GET` `/api/workspace/internals/simulation/{organizationId}/GetSimulationEnvironment/{environmentId}`
- `POST` `/api/workspace/internals/simulation/{organizationId}/CreateSimulationRuns`
- `POST` `/api/workspace/internals/simulation/{organizationId}/CreateSimulationRunsInSingleApp`
- `POST` `/api/workspace/internals/simulation/{organizationId}/CreateSimulationRunsWithInputs`

## Slice

- `GET` `/api/workspace/{applicationId}/slice/Get/{sliceConfigurationId}`
- `POST` `/api/workspace/{applicationId}/slice/Create`
- `POST` `/api/workspace/{applicationId}/slice/Delete/{sliceConfigurationId}`
- `POST` `/api/workspace/{applicationId}/slice/ListForApplication`
- `POST` `/api/workspace/{applicationId}/slice/Update/{sliceConfigurationId}`

## Spreadsheet

- `DELETE` `/api/workspace/{applicationId}/spreadsheet/DeleteFromView/{viewId}`
- `POST` `/api/workspace/{applicationId}/spreadsheet/GetOrCreate`
- `POST` `/api/workspace/{applicationId}/spreadsheet/Update`

## Sublist

- `POST` `/api/workspace/{applicationId}/sublist/CreateSublistFrom`

## Table

- `DELETE` `/api/workspace/{applicationId}/table/Remove/{tableId}`
- `GET` `/api/workspace/{applicationId}/table/Get/{tableId}`
- `GET` `/api/workspace/{applicationId}/table/GetUsages/{tableId}`
- `GET` `/api/workspace/{applicationId}/table/List`
- `POST` `/api/workspace/table/{organizationId}/FindSomeForOrganization`
- `POST` `/api/workspace/{applicationId}/table/CreateWithDefaultView`
- `POST` `/api/workspace/{applicationId}/table/DuplicateTable`
- `POST` `/api/workspace/{applicationId}/table/FindTableInputDropdownItems/{tableId}`
- `POST` `/api/workspace/{applicationId}/table/MoveIntoFolder/{tableId}`
- `POST` `/api/workspace/{applicationId}/table/RenameSome`
- `PUT` `/api/workspace/{applicationId}/table/ChangeAiMetadata/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/ChangeDescription/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/Consolidate/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/Rename/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/SetDefaultView/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/SetDisplayNames/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/SetInputDropdownFilterConfig/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/ToggleManualSave/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/Unconsolidate/{tableId}`
- `PUT` `/api/workspace/{applicationId}/table/Update/{tableId}`

## TableInternal

- `GET` `/api/workspace/internals/consolidation/DisableConsolidation/{organizationId}`
- `GET` `/api/workspace/internals/consolidation/EnableConsolidation/{organizationId}`
- `GET` `/api/workspace/internals/consolidation/GetAll/{organizationId}`
- `GET` `/api/workspace/internals/consolidation/QueryTableConsolidationMappings`
- `PUT` `/api/workspace/internals/consolidation/Consolidate/{organizationId}/{applicationId}/{tableId}`
- `PUT` `/api/workspace/internals/consolidation/DisableConsolidationForApplication/{organizationId}/{applicationId}`
- `PUT` `/api/workspace/internals/consolidation/SetCustomChunkConfigurations/{organizationId}/{applicationId}/{tableId}`
- `PUT` `/api/workspace/internals/consolidation/SetDisableConsolidationFlag/{organizationId}/{applicationId}/{tableId}`
- `PUT` `/api/workspace/internals/consolidation/Unconsolidate/{organizationId}/{applicationId}/{tableId}`

## User

- `DELETE` `/api/workspace/user/DeleteFavorite/{favoriteId}`
- `GET` `/api/workspace/user/GetUserPreferences/{organizationId}`
- `POST` `/api/workspace/user/FindSomeUserPreferences/{organizationId}`
- `PUT` `/api/workspace/user/AddFavorite`

## UserExportV1

- `POST` `/api/workspace/{applicationId}/user_export/ExportTableDataV1/table/{tableId}`

## UserGroup

- `DELETE` `/api/workspace/usergroup/Remove/{organizationId}/{userGroupId}`
- `GET` `/api/workspace/usergroup/All/{organizationId}`
- `GET` `/api/workspace/usergroup/AllConflicts/{organizationId}`
- `GET` `/api/workspace/usergroup/ExportGroupMembers/{organizationId}`
- `POST` `/api/workspace/usergroup/AddAssignments/{organizationId}`
- `POST` `/api/workspace/usergroup/Create/{organizationId}`
- `POST` `/api/workspace/usergroup/FindSome/{organizationId}`
- `POST` `/api/workspace/usergroup/GetConflictsOfUserGroups/{organizationId}`
- `POST` `/api/workspace/usergroup/ParseUpdateMembersCsv/{organizationId}`
- `POST` `/api/workspace/usergroup/SetAssignmentsInApplication/{organizationId}`
- `PUT` `/api/workspace/usergroup/BatchUpdateMembers/{organizationId}`
- `PUT` `/api/workspace/usergroup/ChangeDescription/{organizationId}/{userGroupId}`
- `PUT` `/api/workspace/usergroup/Rename/{organizationId}/{userGroupId}`
- `PUT` `/api/workspace/usergroup/SetAssignments/{organizationId}/{userGroupId}`
- `PUT` `/api/workspace/usergroup/SetMembers/{organizationId}/{userGroupId}`
- `PUT` `/api/workspace/usergroup/Update/{organizationId}/{userGroupId}`

## UserInternal

- `GET` `/api/workspace/internals/user/GetAllUserPreferences`

## Variable

- `DELETE` `/api/workspace/{organizationId}/{applicationId}/variable/Remove/{variableId}`
- `GET` `/api/workspace/{organizationId}/{applicationId}/variable/Get/{variableId}`
- `GET` `/api/workspace/{organizationId}/{applicationId}/variable/ListAllInApp`
- `POST` `/api/workspace/{organizationId}/{applicationId}/variable/Create`
- `POST` `/api/workspace/{organizationId}/{applicationId}/variable/FindSomeInApplication`
- `POST` `/api/workspace/{organizationId}/{applicationId}/variable/ResolveVariablesByMetricSlices`
- `PUT` `/api/workspace/{organizationId}/{applicationId}/variable/Update/{variableId}`

## View

- `DELETE` `/api/workspace/{applicationId}/view/Remove/{viewId}`
- `GET` `/api/workspace/{applicationId}/view/ExportListData/{viewId}`
- `GET` `/api/workspace/{applicationId}/view/ExportTableData/{viewId}`
- `GET` `/api/workspace/{applicationId}/view/Get/{viewId}`
- `GET` `/api/workspace/{applicationId}/view/MergeDraft/{draftViewId}`
- `POST` `/api/workspace/{applicationId}/getViewUsagesForUnderlyingBlock/{blockId}`
- `POST` `/api/workspace/{applicationId}/view/Create`
- `POST` `/api/workspace/{applicationId}/view/CreateFromArmSetExplorer`
- `POST` `/api/workspace/{applicationId}/view/CreateFromDrillDown`
- `POST` `/api/workspace/{applicationId}/view/CreateFromKpi/{viewId}`
- `POST` `/api/workspace/{applicationId}/view/CreateViewWithDefaultConfig`
- `POST` `/api/workspace/{applicationId}/view/ExportViewCsvData/{viewId}`
- `POST` `/api/workspace/{applicationId}/view/FindPageSelectorItems/{viewId}`
- `POST` `/api/workspace/{applicationId}/view/Fork/{viewId}`
- `POST` `/api/workspace/{applicationId}/view/GetDataviz`
- `POST` `/api/workspace/{applicationId}/view/GetDatavizSummaries`
- `POST` `/api/workspace/{applicationId}/view/GetListViewData/{viewId}`
- `POST` `/api/workspace/{applicationId}/view/GetTableViewData/{viewId}`
- `POST` `/api/workspace/{applicationId}/view/ResetCalculationsOrderToDefault/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeCalculationsOrder/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeChartConfig/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeCustomAggregation/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeDescription/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeExtraBreakdownConfig/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeFilterConfig/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeKpiConfig/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeMetricsHeaderOfRowHeaderStyleOptions/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeMetricsPosition/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeOptions/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangePivotFields/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangePivotTableConfig/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeSharingStatus/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeSortConfig/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeValueFields/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/ChangeViewDataPaginationMode/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/PromoteToPublic/{viewId}`
- `PUT` `/api/workspace/{applicationId}/view/Rename/{viewId}`

## ViewApi

- `GET` `/api/v1/views`

## ViewInternal

- `GET` `/api/workspace/internals/view/Get`
- `GET` `/api/workspace/internals/view/GetFeatureUsage`
- `GET` `/api/workspace/internals/view/ListViewsOnBlock`
- `GET` `/api/workspace/internals/view/ListViewsUsingProperty`
- `GET` `/api/workspace/internals/view/UnsafeListViewsUsingProperty`
- `POST` `/api/workspace/internals/view/GarbageCollectExpiredViewDraftsForAllOrganizations`
- `POST` `/api/workspace/internals/view/StartViewBench`
- `POST` `/api/workspace/internals/view/StartViewDiff`
